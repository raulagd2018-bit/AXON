import jwt
from datetime import datetime, timedelta

SECRET_KEY = "clave_super_secreta_axioma_2026_PRO" # Ahora tiene más de 32 caracteres
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    # Token válido por 24 horas
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None
