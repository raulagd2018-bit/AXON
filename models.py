from datetime import datetime
from typing import Optional
from pydantic import EmailStr, Field
from beanie import Document

class User(Document):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)
    phone_number: str
    hashed_password: str
    is_verified: bool = False
    role: str = "USER"  # Puede ser USER, CREATOR, o ADMIN
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users" # Así se llamará la colección en tu MongoDB
