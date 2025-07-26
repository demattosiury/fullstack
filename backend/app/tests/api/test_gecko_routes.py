import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from unittest.mock import patch, AsyncMock

from app.models.gecko import GeckoWaitingTimeResponse
from app.api.gecko_routes import router


app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_get_gecko_status():
    """
    Testa se a rota /status retorna status 200 e o modelo esperado.
    """
    headers = {"Authorization": "Bearer faketoken123"}
    mock_status = {"gecko_says": "(V3) To the Moon!"}

    with patch("app.api.gecko_routes.decode_token"), patch(
        "app.api.gecko_routes.fetch_status",
        new=AsyncMock(return_value=mock_status),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/gecko/status", headers=headers)

            assert response.status_code == 200
            assert response.json() == mock_status

@pytest.mark.anyio
async def test_tempo_restante_importacao_true():
    """
    Testa se a rota /tempo-importar retorna status 200 e o modelo esperado.
    """
    headers = {"Authorization": "Bearer faketoken123"}
    mock_response = GeckoWaitingTimeResponse(waiting_time=0, can_import=True)

    with patch(
        "app.api.gecko_routes.decode_token"  # ),patch("app.api.gecko_routes.fetch_coins_market",new=AsyncMock(return_value=mock_value),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/gecko/tempo-importar", headers=headers)

            assert response.status_code == 200
            assert response.json() == mock_response.model_dump()

@pytest.mark.anyio
async def test_importar_moedas():
    """
    Testa se a rota /importar retorna status 201 e o modelo esperado.
    """
    headers = {"Authorization": "Bearer faketoken123"}
    mock_value = 10
    mock_response = {"message": "10 moedas importadas com sucesso."}

    with patch("app.api.gecko_routes.get_db"), patch(
        "app.api.gecko_routes.decode_token"
    ), patch(
        "app.api.gecko_routes.fetch_coins_market",
        new=AsyncMock(return_value=mock_value),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/gecko/importar", headers=headers)

            assert response.status_code == 201
            assert response.json() == mock_response


@pytest.mark.anyio
async def test_tempo_restante_importacao_false():
    """
    Testa se a rota /tempo-importar retorna status 200 e o modelo esperado.
    """
    headers = {"Authorization": "Bearer faketoken123"}
    mock_response = GeckoWaitingTimeResponse(waiting_time=120, can_import=False)

    with patch(
        "app.api.gecko_routes.decode_token"  # ),patch("app.api.gecko_routes.fetch_coins_market",new=AsyncMock(return_value=mock_value),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/gecko/tempo-importar", headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert data['waiting_time'] < mock_response.waiting_time
