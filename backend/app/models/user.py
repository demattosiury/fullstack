from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from app.core.database import Base



# SQLAlchemy model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    api_key = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

# Pydantic DTOs
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    api_key: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    api_key: str

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: EmailStr
    api_key: str
    old_password: str
    new_password: str