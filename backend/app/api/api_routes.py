from fastapi import APIRouter, HTTPException, status
import logging

logger = logging.getLogger("app.api.api_routes")
router = APIRouter(prefix="/api", tags=["api"])

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
