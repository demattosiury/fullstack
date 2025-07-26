from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
import logging

from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.core.security import get_password_hash, verify_password

# Logger específico para operações de usuário
logger = logging.getLogger("app.services.user_service")


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Busca um usuário no banco de dados pelo e-mail.

    Args:
        db (AsyncSession): Sessão assíncrona do banco de dados.
        email (str): E-mail do usuário.

    Returns:
        Optional[User]: Usuário encontrado ou None.
    """
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


async def create_user(db: AsyncSession, user_in: UserCreate) -> UserRead:
    """
    Cria um novo usuário no banco de dados.

    Args:
        db (AsyncSession): Sessão do banco de dados.
        user_in (UserCreate): Dados do novo usuário.

    Returns:
        UserRead: Representação de leitura do usuário criado.
    """
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


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[UserRead]:
    """
    Autentica um usuário com base em e-mail e senha.

    Args:
        db (AsyncSession): Sessão do banco.
        email (str): E-mail fornecido.
        password (str): Senha fornecida.

    Returns:
        Optional[UserRead]: Usuário autenticado ou None.
    """
    logger.info("Autenticando usuário...")
    try:
        user = await get_user_by_email(db, email)

        if user and verify_password(password, user.hashed_password):
            logger.info("Autenticação de usuário com sucesso.")
            return UserRead.model_validate(user)
        else:
            logger.warning("Falha na autenticação de usuário.")
            return None
    except Exception as e:
        logger.error(f"Erro ao autenticar usuário: {e}", exc_info=True)
        raise


async def update_user_api_key(
    db: AsyncSession, user_to_update: UserUpdate
) -> Optional[UserRead]:
    """
    Atualiza a chave de API de um usuário autenticado.

    Args:
        db (AsyncSession): Sessão do banco.
        user_to_update (UserUpdate): Dados do usuário e nova chave.

    Returns:
        Optional[UserRead]: Usuário atualizado ou None se falhar.
    """
    logger.info(f"Atualizando api_key do usuário: {user_to_update.email}...")
    try:
        user = await authenticate_user(
            db, user_to_update.email, user_to_update.old_password
        )

        if user:
            # user.hashed_password = get_password_hash(user_to_update.new_password)
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
