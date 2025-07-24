import pytest
from unittest.mock import AsyncMock, Mock, patch

from app.services.gecko import fetch_status, PING_URL
from app.models.gecko import GeckoStatusResponse

@pytest.mark.asyncio
@patch("app.services.gecko.httpx.AsyncClient.get")
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

    mock_get.assert_called_once_with(PING_URL)
    assert isinstance(result, GeckoStatusResponse)
    assert result.gecko_says == "(V3) To the Moon!"
