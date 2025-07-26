import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

from app.services.indicators_service import (
    get_latest_coins_and_indicators,
    calculate_indicators,
)
from app.models.gecko import Cryptocurrency


def test_calculate_indicators_basic_case():
    """
    Testa se os indicadores são corretamente calculados para um objeto válido de Cryptocurrency.
    """
    coin = Cryptocurrency(
        coingecko_id="bitcoin",
        name="Bitcoin",
        symbol="BTC",
        ath=70000,
        current_price=65000,
        low_24h=60000,
        total_volume=30000000000,
        market_cap=1000000000000,
        ath_date=datetime.utcnow() - timedelta(days=100),
        last_updated=datetime.utcnow(),
        total_supply=21000000,
        max_supply=21000000,
    )

    indicators = calculate_indicators(coin)

    assert indicators.coingecko_id == "bitcoin"
    assert indicators.percent_off_ath > 0
    assert indicators.price_to_24h_low_ratio == 65000 / 60000
    assert indicators.volume_to_market_cap_ratio == 30000000000 / 1000000000000
    assert indicators.days_since_ath == 100
    assert indicators.hypothetical_total_value == 65000 * 21000000


@pytest.mark.asyncio
async def test_get_latest_coins_and_indicators_returns_data():
    mock_coin = Cryptocurrency(
        id=1,
        coingecko_id="bitcoin",
        symbol="BTC",
        name="Bitcoin",
        image="https://example.com/image.png",
        current_price=65000.0,
        market_cap=1000000000000,
        market_cap_rank=1,
        fully_diluted_valuation=1100000000000,
        total_volume=30000000000,
        high_24h=66000.0,
        low_24h=60000.0,
        price_change_24h=500.0,
        price_change_percentage_24h=0.77,
        market_cap_change_24h=5000000000,
        market_cap_change_percentage_24h=0.5,
        circulating_supply=19500000,
        total_supply=21000000,
        max_supply=21000000,
        ath=70000.0,
        ath_change_percentage=-7.14,
        ath_date=datetime(2024, 1, 1),
        atl=65.0,
        atl_change_percentage=99900.0,
        atl_date=datetime(2013, 1, 1),
        last_updated=datetime(2024, 4, 1),
        imported_at=datetime(2024, 4, 1),
    )

    # Mock da chamada scalars().all()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [mock_coin]

    mock_execute_result = MagicMock()
    mock_execute_result.scalars.return_value = mock_scalars

    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_execute_result

    result = await get_latest_coins_and_indicators(mock_db)

    assert len(result.coins) == 1
    assert result.coins[0].coingecko_id == "bitcoin"
    assert len(result.coins_indicators) == 1
    assert result.coins_indicators[0].coingecko_id == "bitcoin"
