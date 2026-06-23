# app/models/__init__.py
from .user import UserBase, UserCreate, UserInDB

# Si en auth.py necesitas "User", puedes hacer un alias aquí:
User = UserInDB 

__all__ = ["UserBase", "UserCreate", "UserInDB", "User"]
