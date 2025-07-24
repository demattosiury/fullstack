from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional
import os
import logging 

logger = logging.getLogger("app.core.security")

SECRET_KEY = os.getenv("API_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
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
        
def get_password_hash(password):
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
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.error(f"Erro ao gerar token de acesso: {e}", exc_info=True)
        raise

def decode_token(token: str):
    logger.info("Decodificando token de acesso...")
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        logger.error(f"Erro ao decodificar token de acesso: {e}", exc_info=True)
        raise