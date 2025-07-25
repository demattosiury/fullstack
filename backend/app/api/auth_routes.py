from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserRead
from app.core.database import get_db
from app.services.user_service import create_user, authenticate_user, get_user_by_email
from app.core.security import create_access_token
from datetime import timedelta
import logging

logger = logging.getLogger("app.api.auth_routes")
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/registrar", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info("Requisição para criar novo usuário...")
    try:
        if await get_user_by_email(db, user.email):
            logger.warning("E-mail em uso.")
            raise HTTPException(status_code=409, detail="E-mail em uso.")
        
        new_user = await create_user(db, user)

        if new_user:
            logger.info(f"Usuário criado com sucesso: {new_user.email}")
            return new_user
        else:
            logger.warning(f"Usuário não foi criado: {new_user.email}")
            raise HTTPException(status_code=500, detail="Erro interno do servidor.")
    except HTTPException:
        raise  # repassa erros HTTP para FastAPI tratar
    except Exception as e:
        logger.error(f"Erro na requisição para criar novo usuário: {e}",exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    logger.info(f"Requisição para autenticar usuário: {form_data.username}")
    try:
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Dados inválidos.")
        
        access_token = create_access_token(
            data={"sub": str(user.email), "api_key":str(user.api_key)}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise  # repassa erros HTTP para FastAPI tratar
    except Exception as e:
        logger.error(f"Erro na requisição para autenticar usuário ({form_data.username}): {e}",exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")