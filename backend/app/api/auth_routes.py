# app/api/auth_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import logging

from app.models.user import UserCreate, UserRead, UserWithToken, BearerToken
from app.core.database import get_db
from app.services.user_service import (
    create_user,
    authenticate_user,
    get_user_by_email,
)
from app.core.security import create_access_token

# Configuração do logger
logger = logging.getLogger("app.api.auth_routes")

# Roteador de autenticação
router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "/registrar",
    response_model=UserWithToken,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria um novo usuário e retorna o token de autenticação.",
)
async def registrar(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info("Solicitação de registro recebida.")

    try:
        existing_user = await get_user_by_email(db, user.email)
        if existing_user:
            logger.warning("Tentativa de registro com e-mail já em uso.")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado."
            )

        new_user = await create_user(db, user)

        if not new_user:
            logger.error("Falha ao criar usuário. Retornou None.")
            raise HTTPException(
                status_code=500, detail="Erro interno ao criar usuário."
            )

        access_token = create_access_token(
            data={"sub": new_user.email, "api_key": new_user.api_key}
        )

        logger.info(f"Usuário registrado com sucesso: {new_user.email}")
        return UserWithToken(**new_user.model_dump(), access_token=access_token)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado no registro de usuário: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor.",
        )


@router.post(
    "/login",
    summary="Login do usuário",
    description="Autentica um usuário e retorna o token de acesso.",
    response_model=BearerToken,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    logger.info(f"Tentativa de login para: {form_data.username}")

    try:
        user = await authenticate_user(db, form_data.username, form_data.password)

        if not user:
            logger.warning("Falha de autenticação: credenciais inválidas.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos.",
            )

        access_token = create_access_token(
            data={"sub": user.email, "api_key": user.api_key}
        )

        logger.info(f"Usuário autenticado com sucesso: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro durante login do usuário: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor.",
        )
