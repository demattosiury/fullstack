from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.core.security import decode_token, oauth2_scheme
from app.models.user import UserRead, UserUpdate
from app.core.database import get_db
from app.services.user_service import get_user_by_email, update_user_api_key

# Configuração do logger
logger = logging.getLogger("app.api.user_routes")

# Roteador de autenticação
router = APIRouter(prefix="/user", tags=["Usuário"])


@router.get(
    "/info",
    response_model=UserRead,
    summary="Obter informações do usuário autenticado",
    description="Retorna os dados do usuário extraídos do token JWT.",
)
async def read_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    logger.info("Requisição para ler dados do usuário...")
    try:
        payload = decode_token(token)
        user_email: str = payload.get("sub")

        if not user_email:
            logger.warning("Token sem email válido.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido."
            )

        user = await get_user_by_email(db, user_email)

        if not user:
            logger.info("Usuário não encontrado.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
            )

        logger.info(f"Retornando dados do usuário {user_email}.")
        return UserRead(id=user.id, email=user.email, api_key=user.api_key)

    except HTTPException:
        raise  # repassa erros HTTP para FastAPI tratar
    except Exception as e:
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor.",
        )


@router.put(
    "/atualizar/api_key",
    response_model=UserRead,
    summary="Atualizar a API Key do usuário",
    description="Atualiza a API Key do usuário autenticado com base no email contido no token JWT.",
)
async def update_user(
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    logger.info("Requisição para atualizar dados do usuário...")
    try:
        payload = decode_token(token)
        user_email: str = payload.get("sub")
        user.email = user_email

        if not user_email:
            logger.warning("Token sem email válido.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido."
            )

        user = await update_user_api_key(db, user)

        if not user:
            logger.info("Usuário não encontrado.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
            )

        logger.info(f"Retornando dados do usuário {user_email}.")
        return UserRead(id=user.id, email=user.email, api_key=user.api_key)

    except HTTPException:
        raise  # repassa erros HTTP para FastAPI tratar
    except Exception as e:
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor.",
        )
