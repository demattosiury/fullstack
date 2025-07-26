from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional
import logging

logger = logging.getLogger("app.services.user_service")


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    logger.info("Buscando usuário por e-mail...")
    try:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            logger.info("Encontrado usuário por e-mail.")
        else:
            logger.warning("Usuário não encontrado.")
        return user
    except Exception as e:
        logger.error(f"Erro ao buscar usuário por e-mail: {e}", exc_info=True)
        raise


async def create_user(db: AsyncSession, user_in: UserCreate):
    logger.info("Criando novo usuário...")
    try:
        hashed_pw = get_password_hash(user_in.password)
        user = User(
            email=user_in.email, api_key=user_in.api_key, hashed_password=hashed_pw
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return UserRead.model_validate(user)
    except Exception as e:
        logger.error(f"Erro ao criar novo usuário: {e}", exc_info=True)
        raise


async def authenticate_user(db: AsyncSession, email: str, password: str):
    logger.info("Autenticando usuário...")
    try:
        user = await get_user_by_email(db, email)

        if user and verify_password(password, user.hashed_password):
            logger.info("Autenticação de usuário com sucesso.")
            return user
        else:
            logger.warning("Falha na autenticação de usuário.")
            return None
    except Exception as e:
        logger.error(f"Erro ao autenticar usuário: {e}", exc_info=True)
        raise


async def update_user_api_key(db: AsyncSession, user_to_update: UserUpdate):
    logger.info(f"Atualizando api_key do usuário: {user_to_update.email}...")
    try:
        user = await authenticate_user(
            db, user_to_update.email, user_to_update.old_password
        )

        if user:
            #user.hashed_password = get_password_hash(user_to_update.new_password)
            user.api_key = user_to_update.api_key

            await db.commit()
            await db.refresh(user)
            return user
        else:
            logger.warning("Falha ao atualizar usuário.")
            return None
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário: {e}", exc_info=True)
        raise
