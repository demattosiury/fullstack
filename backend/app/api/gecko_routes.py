from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import decode_token
import logging
from fastapi.security import OAuth2PasswordBearer
from app.services.gecko_service import fetch_status, fetch_coins_market
from app.models.gecko import GeckoStatusResponse
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

logger = logging.getLogger("app.api.gecko_routes")
router = APIRouter(prefix="/gecko", tags=["gecko"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Variável global para armazenar o último horário de importação
last_global_import: datetime | None = None


@router.get("/status", response_model=GeckoStatusResponse)
async def get_gecko_status(token: str = Depends(oauth2_scheme)):
    logger.info(f"Buscando o status da GeckoCoinAPI...")
    try:
        payload = decode_token(token)
        user_email: str = payload.get("sub")

        if not user_email:
            logger.warning("Token sem email válido.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido."
            )

        gecko_status = await fetch_status()
        logger.info(f"Retornando status da GeckoCoinAPI.")
        return gecko_status

    except HTTPException:
        raise  # repassa erros HTTP para FastAPI tratar
    except Exception as e:
        logger.error(f"Error ao buscar status da GeckoCoinAPI: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor.",
        )

@router.get("/tempo-importar")
async def tempo_restante_importacao(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_email = payload.get("sub")

        if not user_email:
            logger.warning("Token inválido sem email.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")

        now = datetime.now(timezone.utc)
        if not last_global_import:
            return {"tempo_restante": 0, "pode_importar": True}

        diff = now - last_global_import
        minutos_passados = diff.total_seconds() / 60

        if minutos_passados >= 15:
            return {"tempo_restante": 0, "pode_importar": True}
        else:
            restante = int(15 - minutos_passados)
            return {"tempo_restante": restante, "pode_importar": False}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao verificar tempo restante para importar: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")

@router.post("/importar", status_code=201)
async def importar_moedas(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    try:

        global last_global_import

        payload = decode_token(token)
        user_email: str = payload.get("sub")
        api_key: str = payload.get("api_key")

        if not user_email or not api_key:
            logger.warning("Token inválido ou sem api_key.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido."
            )

        now = datetime.now(timezone.utc)

        if last_global_import and now - last_global_import < timedelta(minutes=15):
            waiting_time = 15 - int((now - last_global_import).total_seconds() // 60)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Importação já realizada. Tente novamente em ~{waiting_time} minuto(s).",
            )

        total = await fetch_coins_market(api_key=api_key, db=db)
        last_global_import = now

        logger.info(
            f"Importação realizada com sucesso para usuário {user_email}, {total} moedas importadas."
        )
        return {"message": f"{total} moedas importadas com sucesso."}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao importar moedas: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor.",
        )
