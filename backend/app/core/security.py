from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional
import os
import logging
from dotenv import load_dotenv

# Logger dedicado para segurança/autenticação
logger = logging.getLogger("app.core.security")


# Carrega variáveis de ambiente
load_dotenv()

# Chave secreta para geração de tokens JWT
SECRET_KEY = os.getenv("API_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Dependência do FastAPI para autenticação via OAuth2 (utiliza JWT)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login", scheme_name="OAuth2PasswordBearer"
)

# Configuração do contexto de hashing de senhas (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.

    Args:
        plain_password (str): Senha em texto plano fornecida pelo usuário.
        hashed_password (str): Hash da senha armazenado no banco.

    Returns:
        bool: True se a senha for válida, False caso contrário.
    """
    logger.info("Validando senha...")
    try:
        if pwd_context.verify(plain_password, hashed_password):
            logger.info("Senha válida.")
            return True
        else:
            logger.info("Senha inválida.")
            return False
    except Exception as e:
        logger.error(f"Erro ao validar senha: {e}", exc_info=True)
        raise


def get_password_hash(password: str) -> str:
    """
    Gera um hash seguro para a senha fornecida.

    Args:
        password (str): Senha em texto plano.

    Returns:
        str: Hash da senha.
    """
    logger.info("Transformando senha em hash...")
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Erro ao transformar senha em hash: {e}", exc_info=True)
        raise


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    logger.info("Gerando token de acesso...")
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.error(f"Erro ao gerar token de acesso: {e}", exc_info=True)
        raise


def decode_token(token: str) -> dict:
    """
    Decodifica e valida um token JWT.

    Args:
        token (str): Token JWT a ser decodificado.

    Returns:
        dict: Dados contidos no token.

    Raises:
        JWTError: Se o token for inválido ou expirado.
    """
    logger.info("Decodificando token de acesso...")
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        logger.error(f"Erro ao decodificar token de acesso: {e}", exc_info=True)
        raise
