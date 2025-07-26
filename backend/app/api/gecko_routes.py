from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import time
import logging
import os
from dotenv import load_dotenv

from app.core.security import decode_token, oauth2_scheme
from app.services.gecko_service import fetch_status, fetch_coins_market
from app.models.gecko import (
    GeckoStatusResponse,
    GeckoWaitingTimeResponse,
    GeckoImportResponse,
)
from app.core.database import get_db

# Configuração do logger
logger = logging.getLogger("app.api.gecko_routes")

# Roteador de autenticação
router = APIRouter(prefix="/gecko", tags=["CoinGeckoAPI"])


# Variável global para armazenar o último horário de importação
last_global_import: float | None = None


load_dotenv()
# Variável global para armazenar quantos segundos de espera
SECONDS: int = int(os.getenv("COINGECKO_SECONDS"))


@router.get(
    "/status",
    response_model=GeckoStatusResponse,
    summary="Health Check da CoinGeckoAPI",
    description="Endpoint simples para verificar se a API está ativa (health check).Retorna '(V3) To the Moon!' em caso de sucesso.",
)
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


@router.get(
    "/tempo-importar",
    response_model=GeckoWaitingTimeResponse,
    summary="Tempo restante para nova importação",
    description=f"Verifica se já se passaram {SECONDS} segundos desde a última importação de moedas.",
)
async def tempo_restante_importacao(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_email = payload.get("sub")

        if not user_email:
            logger.warning("Token inválido sem email.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido."
            )

        now = time.time()
        if not last_global_import:
            return GeckoWaitingTimeResponse(waiting_time=0, can_import=True)

        elapsed = now - last_global_import

        if elapsed >= SECONDS:
            return GeckoWaitingTimeResponse(waiting_time=0, can_import=True)
        else:
            return GeckoWaitingTimeResponse(
                waiting_time=int(SECONDS - elapsed), can_import=False
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Erro ao verificar tempo restante para importar: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor.",
        )


@router.post(
    "/importar",
    response_model=GeckoImportResponse,
    status_code=201,
    summary="Importar moedas do CoinGecko",
    description=f"Importa moedas e indicadores, limitado a 1 chamada a cada {SECONDS} segundos.",
)
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

        now = time.time()

        if last_global_import:
            elapsed = now - last_global_import
            if elapsed < SECONDS:
                waiting_time = int(SECONDS - elapsed)
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Importação já realizada. Tente novamente em ~{waiting_time} segundos(s).",
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
