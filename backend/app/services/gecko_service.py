import httpx
import os
import logging
from typing import Optional
from dotenv import load_dotenv
from app.models.gecko import GeckoStatusResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.gecko import Cryptocurrency
from datetime import datetime, timezone

load_dotenv()
BASE_URL = os.getenv("COINGECKO_BASE_URL")
PING_URL = f"{BASE_URL}/ping"
#COINS_URL = f"{BASE_URL}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=1&page=1"

logger = logging.getLogger("app.services.gecko")


async def fetch_from_api(url: str, api_key: Optional[str] = None) -> dict:
    headers = {}
    if api_key:
        headers = {"accept": "application/json"}#, "x-cg-pro-api-key": api_key}
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Requisitando {url}")
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            logger.info("Resposta recebida com sucesso.")
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Erro HTTP ao requisitar {url}: {e.response.status_code}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao requisitar {url}: {e}", exc_info=True)
        raise


async def fetch_status() -> GeckoStatusResponse:
    logger.info(f"Requisitando health check da GeckoCoinAPI.")
    try:
        data = await fetch_from_api(PING_URL)
        return GeckoStatusResponse(**data)
    except Exception:
        logger.error("Erro ao consumir endpoint de status da GeckoCoinAPI.")
        raise


async def persist_coins(coins: list[dict], db: AsyncSession) -> int:
    total = 0

    try:
        for coin in coins:

            ath_date = datetime.fromisoformat(coin.get("ath_date")).replace(tzinfo=None)
            atl_date = datetime.fromisoformat(coin.get("atl_date")).replace(tzinfo=None)
            last_updated = datetime.fromisoformat(coin.get("last_updated")).replace(tzinfo=None)

            new = Cryptocurrency(
                coingecko_id=coin.get("id"),
                name=coin.get("name"),
                symbol=coin.get("symbol"),
                image=coin.get("image"),
                current_price=coin.get("current_price"),
                market_cap=coin.get("market_cap"),
                market_cap_rank=coin.get("market_cap_rank"),
                fully_diluted_valuation=coin.get("fully_diluted_valuation"),
                total_volume=coin.get("total_volume"),
                high_24h=coin.get("high_24h"),
                low_24h=coin.get("low_24h"),
                price_change_24h=coin.get("price_change_24h"),
                price_change_percentage_24h=coin.get("price_change_percentage_24h"),
                market_cap_change_24h=coin.get("market_cap_change_24h"),
                market_cap_change_percentage_24h=coin.get(
                    "market_cap_change_percentage_24h"
                ),
                circulating_supply=coin.get("circulating_supply"),
                total_supply=coin.get("total_supply"),
                max_supply=coin.get("max_supply"),
                ath=coin.get("ath"),
                ath_change_percentage=coin.get("ath_change_percentage"),
                ath_date=ath_date,
                atl=coin.get("atl"),
                atl_change_percentage=coin.get("atl_change_percentage"),
                atl_date=atl_date,
                last_updated=last_updated,
                imported_at=datetime.now(timezone.utc).replace(tzinfo=None)
            )
            db.add(new)
            total += 1

        await db.commit()
        logger.info(f"{total} moedas importadas com sucesso.")
        return total

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Erro ao importar moedas: {e}", exc_info=True)
        raise


async def fetch_coins_market(api_key: str, db) -> int:
    logger.info(f"Requisitando mercado de moedas da GeckoCoinAPI.")
    try:
        url = f"{BASE_URL}/coins/markets?x_cg_demo_api_key={api_key}&vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
        coins = await fetch_from_api(url=url, api_key=api_key)
        total = await persist_coins(coins, db)
        return total
    except Exception as e:
        logger.error(f"Erro ao buscar e importar moedas: {e}", exc_info=True)
        raise
