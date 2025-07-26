import pytest
from unittest.mock import AsyncMock, Mock, MagicMock, patch

from app.services.gecko_service import (
    fetch_status,
    fetch_coins_market,
    PING_URL,
    BASE_URL,
)
from app.models.gecko import GeckoStatusResponse


@pytest.mark.asyncio
@patch("app.services.gecko_service.httpx.AsyncClient.get")
async def test_fetch_status(mock_get):
    """
    Testa se o serviço gecko retorna o modelo esperado
    quando fetch_status é mockado corretamente.
    """
    mock_response = AsyncMock()
    mock_response.json = Mock(return_value={"gecko_says": "(V3) To the Moon!"})
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = await fetch_status()

    mock_get.assert_called_once_with(PING_URL, headers={})
    assert isinstance(result, GeckoStatusResponse)
    assert result.gecko_says == "(V3) To the Moon!"


@pytest.mark.asyncio
@patch("app.services.gecko_service.persist_coins", new_callable=AsyncMock)
@patch("app.services.gecko_service.fetch_from_api", new_callable=AsyncMock)
async def test_fetch_coins_market(mock_fetch_from_api, mock_persist_coins):
    """
    Testa se o serviço gecko retorna o modelo esperado
    quando fetch_coins_market é mockado corretamente.
    """

    mock_coin_data = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "image": "<https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1696501400>",
            "current_price": 70187,
            "market_cap": 1381651251183,
            "market_cap_rank": 1,
            "fully_diluted_valuation": 1474623675796,
            "total_volume": 20154184933,
            "high_24h": 70215,
            "low_24h": 68060,
            "price_change_24h": 2126.88,
            "price_change_percentage_24h": 3.12502,
            "market_cap_change_24h": 44287678051,
            "market_cap_change_percentage_24h": 3.31157,
            "circulating_supply": 19675987,
            "total_supply": 21000000,
            "max_supply": 21000000,
            "ath": 73738,
            "ath_change_percentage": -4.77063,
            "ath_date": "2024-03-14T07:10:36.635Z",
            "atl": 67.81,
            "atl_change_percentage": 103455.83335,
            "atl_date": "2013-07-06T00:00:00.000Z",
            "roi": None,
            "last_updated": "2024-04-07T16:49:31.736Z",
        }
    ]
    apikey = "CG-apikey"

    db = AsyncMock()
    db.add = MagicMock()

    mock_fetch_from_api.return_value = mock_coin_data
    mock_persist_coins.return_value = 1

    result = await fetch_coins_market(db=db, api_key=apikey)

    mock_fetch_from_api.assert_called_once()
    mock_persist_coins.assert_called_once_with(mock_coin_data, db)
    assert result == len(mock_coin_data)
