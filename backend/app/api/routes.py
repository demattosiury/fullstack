from fastapi import APIRouter
import logging

from app.services.gecko import fetch_status
from app.models.gecko import GeckoStatusResponse

router = APIRouter()
logger = logging.getLogger("app.api.routes")

@router.get("/gecko/status", response_model=GeckoStatusResponse)
async def get_gecko_status():
    logger.info(f"Buscando o status da GeckoCoinAPI...")
    try:
        status = await fetch_status()
        logger.info(f"Retornando status da GeckoCoinAPI.")
        return status
    except Exception as e:
        logger.error(f"Error ao buscar status da GeckoCoinAPI: {e}",exc_info=True)
        raise

@router.get("/status", response_model=str)
async def get_status():
    logger.info(f"Buscando o status da API...")
    try:    
        return "Ok!"
    except Exception as e:
        logger.error(f"Error ao buscar status da API: {e}",exc_info=True)
        raise
