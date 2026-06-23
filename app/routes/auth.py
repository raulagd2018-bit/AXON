from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, BaseModel
from typing import Optional
from app.models import User
from app.security.auth import get_password_hash, verify_password, create_access_token

router = APIRouter()

# 1. Esquemas de validación (Pydantic)
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: str

class Token(BaseModel):
    access_token: str
    token_type: str

# 2. Registro Profesional
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    # Verificar si el usuario ya existe
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El correo ya está registrado"
        )
    
    # Crear usuario con contraseña encriptada
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        phone_number=user_data.phone_number,
        hashed_password=get_password_hash(user_data.password)
    )
    await new_user.insert()
    
    return {"message": "Usuario creado exitosamente"}

# 3. Login Profesional (Utilizando OAuth2PasswordRequestForm estándar)
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Buscar usuario
    user = await User.find_one(User.username == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Crear Token JWT
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
