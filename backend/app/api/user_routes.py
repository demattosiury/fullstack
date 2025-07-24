from fastapi import APIRouter, Depends, HTTPException, status
from app.api.auth_routes import router as auth_router
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_token
from app.models.user import UserRead
from app.core.database import get_db

import logging

logger = logging.getLogger("app.api.user_routes")
router = APIRouter(prefix="/user", tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.get("/info", response_model=str)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    logger.info("Requisição para ler dados do usuário...")
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválida.")

    return "Token válida."
