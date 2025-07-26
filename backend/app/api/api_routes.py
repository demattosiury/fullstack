from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.services.indicators_service import get_latest_coins_and_indicators
from app.core.database import get_db

import logging

logger = logging.getLogger("app.api.api_routes")
router = APIRouter(tags=["api"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.get("/status", response_model=str)
async def get_status():
    logger.info(f"Buscando o status da API...")
    try:    
        return "Ok!"
    except HTTPException:
        raise  # repassa erros HTTP para FastAPI tratar
    except Exception as e:
        logger.error(f"Error ao buscar status da API: {e}",exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")

@router.get("/indicadores", response_model=Dict[str, List[Any]])
async def get_coins_and_indicators_endpoint(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retorna uma lista dos registros mais recentes de cada criptomoeda e
    uma lista dos 5 indicadores calculados para esses registros.
    """
    try:
        # Chama a função do serviço que busca os dados e calcula os indicadores
        result = await get_latest_coins_and_indicators(db)
        return result
    except Exception as e:
        logger.error(f"Erro ao buscar moedas e indicadores: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao processar sua requisição."
        )
