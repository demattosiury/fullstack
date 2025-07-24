from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, UserCreate
from app.core.security import get_password_hash, verify_password
import logging

logger = logging.getLogger("app.services.user_service")

async def get_user_by_email(db: AsyncSession, email: str):
    logger.info("Buscando usuário por e-mail...")
    try:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            logger.info("Encontrado usuário por e-mail.")
            return user
        else:
            logger.warning("Usuário não encontrado.")
            return None
    except Exception as e:
        logger.error(f"Erro ao buscar usuário por e-mail: {e}", exc_info=True)
        raise

async def create_user(db: AsyncSession, user_in: UserCreate):
    logger.info("Criando novo usuário...")
    try:
        hashed_pw = get_password_hash(user_in.password)
        user = User(email=user_in.email, hashed_password=hashed_pw)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
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
