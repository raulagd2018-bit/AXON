import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
import os

# Configuración de cifrado de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de seguridad JWT
# RECOMENDACIÓN: En producción, carga estas variables desde un archivo .env
SECRET_KEY = os.getenv("SECRET_KEY", "CAMBIA_ESTO_POR_UNA_LLAVE_MUY_LARGA_Y_ALEATORIA")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera un hash seguro para una contraseña."""
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token con tiempo de expiración configurable.
    data: Diccionario con la información del usuario (claims).
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodifica y valida el token. 
    Retorna el payload si es válido, None si ha expirado o es falso.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Aquí podrías loggear un intento de uso de token expirado
        return None
    except jwt.InvalidTokenError:
        # Aquí podrías loggear un posible ataque (token malformado)
        return None
