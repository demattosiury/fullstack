from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_token
from app.models.user import UserRead, UserUpdate
from app.core.database import get_db
from app.services.user_service import get_user_by_email, update_user_api_key

import logging

logger = logging.getLogger("app.api.user_routes")
router = APIRouter(prefix="/user", tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.get("/info", response_model=UserRead)
async def read_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    logger.info("Requisição para ler dados do usuário...")
    try:
        payload = decode_token(token)
        user_email: str = payload.get("sub")
        
        if not user_email:
            logger.warning("Token sem email válido.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")
        
        user = await get_user_by_email(db,user_email)
        
        if not user:
            logger.info("Usuário não encontrado.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

        logger.info(f"Retornando dados do usuário {user_email}.")
        return UserRead(id=user.id, email=user.email, api_key=user.api_key)
            
    except HTTPException:
        raise  # repassa erros HTTP para FastAPI tratar
    except Exception as e:
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")
    
@router.put("/atualizar/api_key", response_model=UserRead)
async def update_user(user: UserUpdate, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    logger.info("Requisição para atualizar dados do usuário...")
    try:
        payload = decode_token(token)
        user_email: str = payload.get("sub")
        
        if not user_email:
            logger.warning("Token sem email válido.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")
        
        user = await update_user_api_key(db, user)
        
        if not user:
            logger.info("Usuário não encontrado.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

        logger.info(f"Retornando dados do usuário {user_email}.")
        return UserRead(id=user.id, email=user.email, api_key=user.api_key)
            
    except HTTPException:
        raise  # repassa erros HTTP para FastAPI tratar
    except Exception as e:
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")
    