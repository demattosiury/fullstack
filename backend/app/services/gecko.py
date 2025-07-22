import httpx
import os
from dotenv import load_dotenv
from app.models.gecko import GeckoStatusResponse

load_dotenv()
BASE_URL = os.getenv("COINGECKO_BASE_URL")

PING_URL = f'{BASE_URL}/ping'

async def fetch_status() -> GeckoStatusResponse:
     async with httpx.AsyncClient() as client:
        response = await client.get(PING_URL)
        response.raise_for_status()
        data = response.json()
        return GeckoStatusResponse(**data)