# app/api/api_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from app.core.database import get_db
from app.core.security import oauth2_scheme
from app.services.indicators_service import get_latest_coins_and_indicators
from app.models.gecko import IndicatorsResponse

logger = logging.getLogger("app.api.api_routes")

router = APIRouter(
    prefix="",
    tags=["Status e Indicadores"],
    responses={404: {"description": "Não encontrado"}},
)


@router.get(
    "/status",
    response_model=str,
    summary="Health Check da API",
    description="Endpoint simples para verificar se a API está ativa (health check).Retorna 'Ok!' em caso de sucesso.",
)
async def get_status():
    logger.info("Verificando status da API...")
    try:
        return "Ok!"
    except Exception as e:
        logger.error(f"Erro ao verificar status: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor.",
        )


@router.get(
    "/indicadores",
    response_model=IndicatorsResponse,
    summary="Indicadores de Criptomoedas",
    description=(
        "Retorna os registros mais recentes de criptomoedas e uma lista dos "
        "5 principais indicadores calculados com base nesses registros."
        "\n1. Variação Percentual do Preço desde o ATH (All-Time High)"
        "\n2. Razão Preço Atual / Mínima de 24h"
        "\n3. Razão Volume / Capitalização de Mercado"
        "\n4. Dias desde o ATH"
        "\n5. Preço em Relação ao Total Supply"
    ),
)
async def get_coins_and_indicators_endpoint(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    logger.info("Buscando indicadores das criptomoedas...")
    try:
        result = await get_latest_coins_and_indicators(db)
        return result
    except Exception as e:
        logger.error(f"Erro ao buscar indicadores: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar os indicadores.",
        )
