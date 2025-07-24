import httpx
import os
import logging
from dotenv import load_dotenv
from app.models.gecko import GeckoStatusResponse

load_dotenv()
BASE_URL = os.getenv("COINGECKO_BASE_URL")
PING_URL = f'{BASE_URL}/ping'

logger = logging.getLogger("app.services.gecko")

async def fetch_status() -> GeckoStatusResponse:
     try:
      async with httpx.AsyncClient() as client:
         logger.info(f"Consumindo endpoint de status da GeckoCoinAPI...")
         response = await client.get(PING_URL)
         response.raise_for_status()
         data = response.json()
         logger.info(f"Status da GeckoCoinAPI recebido com sucesso.")
         return GeckoStatusResponse(**data)
     except Exception as e:
        logger.error(f"Erro ao consumir endpoint de status da GeckoCoinAPI.")
        raise