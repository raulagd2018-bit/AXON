# app/security/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from .auth import decode_access_token

# Definimos dónde está el endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependencia profesional para proteger rutas.
    Valida el token JWT y retorna el ID del usuario (sub).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o sesión expirada.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Usamos nuestra lógica centralizada en auth.py
    payload = decode_access_token(token)
    
    # Validamos que el token sea válido y contenga el identificador 'sub'
    if payload is None or "sub" not in payload:
        raise credentials_exception
        
    user_id: str = payload.get("sub")
    return user_id

# Opcional: Para implementar niveles de acceso en el futuro
async def get_current_active_user(user_id: str = Depends(get_current_user)):
    # Aquí podrías consultar MongoDB para verificar si el usuario sigue activo
    # o si ha sido baneado.
    return user_id
