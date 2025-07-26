# app/services/indicator_service.py

from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

# Importe seu modelo Cryptocurrency e os schemas
from app.models.gecko import (
    Cryptocurrency,
    CryptocurrencySchema,
    CryptocurrencyIndicatorsSchema,
)


def calculate_indicators(crypto: Cryptocurrency) -> CryptocurrencyIndicatorsSchema:
    """
    Calcula os 5 indicadores para uma criptomoeda.
    """
    percent_off_ath: Optional[float] = None
    price_to_24h_low_ratio: Optional[float] = None
    volume_to_market_cap_ratio: Optional[float] = None
    days_since_ath: Optional[int] = None
    hypothetical_total_value: Optional[float] = None

    # 1. Variação Percentual do Preço desde o ATH (All-Time High)
    if crypto.ath is not None and crypto.ath > 0:
        percent_off_ath = ((crypto.ath - crypto.current_price) / crypto.ath) * 100
        if percent_off_ath < 0:
            percent_off_ath = 0.0

    # 2. Razão Preço Atual / Mínima de 24h
    if crypto.low_24h is not None and crypto.low_24h > 0:
        price_to_24h_low_ratio = crypto.current_price / crypto.low_24h

    # 3. Razão Volume / Capitalização de Mercado
    if (
        crypto.total_volume is not None
        and crypto.market_cap is not None
        and crypto.market_cap > 0
    ):
        volume_to_market_cap_ratio = crypto.total_volume / crypto.market_cap

    # 4. Dias desde o ATH
    # Correção: Use datetime.utcnow() para a data atual, se last_updated não for confiável como "agora"
    # ou use crypto.last_updated se ele realmente reflete a data/hora da consulta.
    # Usaremos crypto.last_updated para consistência com o que está no DB.
    if crypto.ath_date is not None and crypto.last_updated is not None:
        try:
            delta = crypto.last_updated - crypto.ath_date
            days_since_ath = delta.days
        except TypeError:
            days_since_ath = None

    # 5. Preço em Relação ao Total Supply
    if (
        crypto.current_price is not None
        and crypto.total_supply is not None
        and crypto.total_supply > 0
    ):
        hypothetical_total_value = crypto.current_price * crypto.total_supply
    elif (
        crypto.current_price is not None
        and crypto.max_supply is not None
        and crypto.max_supply > 0
    ):
        hypothetical_total_value = crypto.current_price * crypto.max_supply

    return CryptocurrencyIndicatorsSchema(
        coingecko_id=crypto.coingecko_id,
        name=crypto.name,
        symbol=crypto.symbol,
        percent_off_ath=percent_off_ath,
        price_to_24h_low_ratio=price_to_24h_low_ratio,
        volume_to_market_cap_ratio=volume_to_market_cap_ratio,
        days_since_ath=days_since_ath,
        hypothetical_total_value=hypothetical_total_value,
    )


async def get_latest_coins_and_indicators(db: AsyncSession) -> Dict[str, List[Any]]:
    """
    Busca os registros mais recentes (pelo imported_at) de cada criptomoeda no banco de dados,
    calcula seus indicadores e retorna ambos.
    Ambas as listas ('coins' e 'coins_indicators') conterão apenas os registros mais recentes.
    """

    # Subquery para encontrar o `imported_at` mais recente para cada `coingecko_id`
    subquery_stmt = (
        select(
            Cryptocurrency.coingecko_id,
            func.max(Cryptocurrency.imported_at).label("max_imported_at"),
        )
        .group_by(Cryptocurrency.coingecko_id)
        .subquery()
    )

    # Consulta principal para obter os dados completos dos registros MAIS RECENTES
    # que correspondem ao `imported_at` mais recente para cada `coingecko_id`
    latest_coins_stmt = select(Cryptocurrency).join(
        subquery_stmt,
        (Cryptocurrency.coingecko_id == subquery_stmt.c.coingecko_id)
        & (Cryptocurrency.imported_at == subquery_stmt.c.max_imported_at),
    )
    latest_coins_result = await db.execute(latest_coins_stmt)
    latest_coins_records = latest_coins_result.scalars().all()

    # Preparar as listas de retorno, ambas com os registros MAIS RECENTES
    coins_data: List[CryptocurrencySchema] = []
    coins_indicators_data: List[CryptocurrencyIndicatorsSchema] = []

    for coin in latest_coins_records:
        # Adiciona o registro da moeda à lista 'coins' (apenas os mais recentes)
        coins_data.append(CryptocurrencySchema.model_validate(coin))

        # Calcula e adiciona os indicadores à lista 'coins_indicators' (apenas dos mais recentes)
        indicators = calculate_indicators(coin)
        coins_indicators_data.append(indicators)

    return {
        "coins": coins_data,  # Agora contém apenas os registros MAIS RECENTES
        "coins_indicators": coins_indicators_data,  # Contém indicadores apenas dos registros MAIS RECENTES
    }
