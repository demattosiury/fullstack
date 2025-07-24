import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services import user_service
from app.models.user import User, UserCreate

@pytest.mark.asyncio
async def test_get_user_by_email_found():
    mock_user = User(id=1, email="test@example.com", hashed_password="hashed")
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_user
    db.execute.return_value = mock_result

    user = await user_service.get_user_by_email(db, "test@example.com")

    assert user == mock_user
    db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_user_by_email_not_found():
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db.execute.return_value = mock_result

    user = await user_service.get_user_by_email(db, "notfound@example.com")

    assert user is None

@pytest.mark.asyncio
@patch("app.services.user_service.get_password_hash", return_value="hashed_pw")
async def test_create_user_success(mock_hash):
    # `MagicMock` permite misturar métodos síncronos e assíncronos corretamente
    db = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    user_in = UserCreate(email="new@example.com", password="123456")
    
    # Cria um usuário que será retornado por db.refresh
    created_user = User(id=1, email=user_in.email, hashed_password="hashed_pw")

    async def refresh_side_effect(user):
        # Simula o comportamento de atribuição feita internamente pelo refresh
        user.id = created_user.id
        user.email = created_user.email
        user.hashed_password = created_user.hashed_password

    db.refresh.side_effect = refresh_side_effect

    user = await user_service.create_user(db, user_in)

    assert user.email == user_in.email
    assert user.hashed_password == "hashed_pw"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

@pytest.mark.asyncio
@patch("app.services.user_service.verify_password", return_value=True)
@patch("app.services.user_service.get_user_by_email")
async def test_authenticate_user_success(mock_get_user, mock_verify):
    mock_user = User(id=1, email="test@example.com", hashed_password="hashed_pw")
    db = AsyncMock()
    mock_get_user.return_value = mock_user

    user = await user_service.authenticate_user(db, "test@example.com", "123456")

    assert user == mock_user
    mock_get_user.assert_called_once()
    mock_verify.assert_called_once()

@pytest.mark.asyncio
@patch("app.services.user_service.verify_password", return_value=False)
@patch("app.services.user_service.get_user_by_email")
async def test_authenticate_user_fail(mock_get_user, mock_verify):
    mock_user = User(id=1, email="test@example.com", hashed_password="wrong_hash")
    db = AsyncMock()
    mock_get_user.return_value = mock_user

    user = await user_service.authenticate_user(db, "test@example.com", "wrong_pass")

    assert user is None
    mock_get_user.assert_called_once()
    mock_verify.assert_called_once()
