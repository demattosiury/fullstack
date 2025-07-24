import pytest
from datetime import timedelta, datetime, timezone
from jose import jwt


# Supondo que o código esteja no arquivo "security.py"
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
    ALGORITHM,
    SECRET_KEY
)

@pytest.fixture
def password():
    return "teste123"

@pytest.fixture
def hashed_password(password):
    return get_password_hash(password)

def test_verify_password_success(password, hashed_password):
    assert verify_password(password, hashed_password) is True

def test_verify_password_failure(password):
    hashed = get_password_hash("123456")
    assert verify_password(password, hashed) is False

def test_get_password_hash(password):
    hashed = get_password_hash(password)
    assert isinstance(hashed, str)
    assert hashed != password

def test_create_access_token_contains_expected_fields():
    data = {"sub": "user123"}
    token = create_access_token(data)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "user123"
    assert "exp" in decoded

def test_create_access_token_with_explicit_expiration():
    data = {"sub": "user123"}
    delta = timedelta(minutes=10)
    token = create_access_token(data, expires_delta=delta)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    expected_exp = datetime.now(timezone.utc) + delta
    actual_exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    
    # Diferença de no máximo 5 segundos por conta do tempo de execução
    assert abs((actual_exp - expected_exp).total_seconds()) < 5

def test_decode_token_returns_original_data():
    data = {"sub": "user123"}
    token = create_access_token(data)
    decoded = decode_token(token)
    assert decoded["sub"] == "user123"

def test_decode_token_with_invalid_token_raises_exception():
    invalid_token = "teste.teste.teste"
    with pytest.raises(Exception):
        decode_token(invalid_token)
