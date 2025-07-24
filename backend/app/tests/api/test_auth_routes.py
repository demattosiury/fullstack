import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from app.main import app
from app.models.user import User, UserCreate, UserRead, UserLogin

@pytest.mark.asyncio
async def test_register_success():
    fake_user_create = UserCreate(email="teste@exemplo.com", password="123456")
    fake_user_read = UserRead(id=1, email="teste@exemplo.com")

    #fake_user = User(id=1, email="teste@exemplo.com", hashed_password='hashed')

    # Patch nas dependências e serviços
    with patch("app.api.auth_routes.get_user_by_email", return_value=None), \
         patch("app.api.auth_routes.create_user", return_value=fake_user_read), \
         patch("app.api.auth_routes.get_db"):

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/auth/registrar", json={
                "email": fake_user_create.email,
                "password": fake_user_create.password
            })

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == fake_user_read.email

@pytest.mark.asyncio
async def test_login_success():

    fake_user_login = UserLogin(email="teste@exemplo.com", password='senha123')
    fake_user = User(id=1, email="teste@exemplo.com", hashed_password='hashed')

    fake_token = "token.token.token"
    fake_response = {
        "access_token": fake_token,
        "token_type": "bearer"
    }

    # Patch nas dependências e serviços
    with patch("app.api.auth_routes.authenticate_user", return_value=fake_user), \
         patch("app.api.auth_routes.create_access_token", return_value=fake_token):

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/auth/login", data={
                "username": fake_user_login.email,
                "password": fake_user_login.password
            })

        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == fake_response['access_token']
        assert data["token_type"] == fake_response['token_type']