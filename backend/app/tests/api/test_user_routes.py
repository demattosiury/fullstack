import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from unittest.mock import patch, AsyncMock

from app.api.user_routes import router
from app.models.user import User, UserRead


app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_read_user():
    """
    Testa se a rota /info retorna status 200 e o modelo esperado.
    """
    headers = {"Authorization": "Bearer faketoken123"}
    fake_user = User(
        id=1, email="user@exemplo.com", hashed_password="test", api_key="apikey_000"
    )
    fake_user_read = UserRead(id=1,email="user@exemplo.com", api_key="apikey_000")

    with patch("app.api.user_routes.get_db"), patch(
        "app.api.user_routes.decode_token"
    ), patch(
        "app.api.user_routes.get_user_by_email",
        new=AsyncMock(return_value=fake_user),
    ):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/user/info", headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert data['id'] == fake_user_read.id
            assert data['email'] == fake_user_read.email
            assert data['api_key'] == fake_user_read.api_key
