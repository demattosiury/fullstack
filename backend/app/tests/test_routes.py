import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch, AsyncMock
from app.api.routes import router

app = FastAPI()
app.include_router(router)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_get_gecko_status(client):
    """
    Testa se a rota /gecko/status retorna status 200 e o modelo esperado
    quando fetch_status é mockado corretamente.
    """
    mock_response_data = {"gecko_says": "(V3) To the Moon!"}

    with patch("app.api.routes.fetch_status", new_callable=AsyncMock) as mock_fetch_status:
        mock_fetch_status.return_value = mock_response_data

        response = client.get("/gecko/status")

        mock_fetch_status.assert_awaited_once()
        assert response.status_code == 200
        assert response.json() == mock_response_data

def test_get_status(client):
    """
    Testa se a rota /status retorna status 200 e o modelo esperado.
    """
    mock_response_data = "Ok!"

    with patch("app.api.routes.get_status") as mock_fetch_status:
        mock_fetch_status.return_value = mock_response_data

        response = client.get("/status")

        assert response.status_code == 200
        assert response.json() == mock_response_data
