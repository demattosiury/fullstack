import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from unittest.mock import patch, AsyncMock
from app.api.api_routes import router
from app.models.gecko import (
    IndicatorsResponse,
    CryptocurrencySchema,
    CryptocurrencyIndicatorsSchema,
)

app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_get_coins_and_indicators_endpoint():
    """
    Testa se a rota /indicadores retorna status 200 e o modelo esperado.
    """

    mock_data = IndicatorsResponse(
        coins=[
            CryptocurrencySchema(
                id=1,
                coingecko_id="bitcoin",
                symbol="btc",
                name="Bitcoin",
                image="https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
                current_price=64231.12,
                market_cap=1250000000000,
                market_cap_rank=1,
                fully_diluted_valuation=1340000000000,
                total_volume=35000000000,
                high_24h=65000.00,
                low_24h=63000.00,
                price_change_24h=-300.45,
                price_change_percentage_24h=-0.47,
                market_cap_change_24h=-5000000000,
                market_cap_change_percentage_24h=-0.4,
                circulating_supply=19500000,
                total_supply=21000000,
                max_supply=21000000,
                ath=69000.00,
                ath_change_percentage=-6.8,
                ath_date="2021-11-10T14:24:00Z",
                atl=67.81,
                atl_change_percentage=94400.0,
                atl_date="2013-07-06T00:00:00Z",
                last_updated="2025-07-26T12:00:00Z",
                imported_at="2025-07-26T12:05:00Z",
            )
        ],
        coins_indicators=[
            CryptocurrencyIndicatorsSchema(
                coingecko_id="bitcoin",
                name="Bitcoin",
                symbol="btc",
                percent_off_ath=-6.8,
                price_to_24h_low_ratio=1.03,
                volume_to_market_cap_ratio=0.028,
                days_since_ath=987,
                hypothetical_total_value=123456789.0,
            )
        ],
    )

    headers = {"Authorization": "Bearer faketoken123"}

    with patch(
        "app.api.api_routes.get_latest_coins_and_indicators",
        new=AsyncMock(return_value=mock_data),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/indicadores", headers=headers)

            assert response.status_code == 200
            assert len(response.json()) == len(mock_data.model_dump())


def test_status_ok(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.text.strip('"') == "Ok!"
