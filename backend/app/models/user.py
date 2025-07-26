from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from app.core.database import Base


# SQLAlchemy model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    api_key = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)


# Pydantic DTOs
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    api_key: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "email": "joao@email.com",
                "password": "SenhaForte123",
                "api_key": "CG-chave-api-123",
            }
        },
    }


class UserRead(BaseModel):
    id: int
    email: EmailStr
    api_key: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {"id": 1, "email": "joao@email.com", "name": "João da Silva"}
        },
    }


class UserWithToken(UserRead):
    api_key: str
    access_token: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "joao@email.com",
                "name": "João da Silva",
                "api_key": "CG-chave-api-123",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }
    }


class BearerToken(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr
    api_key: str
    old_password: str
    new_password: str
