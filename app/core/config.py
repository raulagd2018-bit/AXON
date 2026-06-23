from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Configuración de Servidor
    DEBUG: bool = True
    
    # Configuración de Base de Datos
    DATABASE_URL: str = "mongodb://localhost:27017"
    
    # Seguridad y JWT
    SECRET_KEY: str = "tu_clave_super_secreta_y_larga"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuración de Pydantic v2
    # 'extra="ignore"' evita que el sistema explote si hay variables extra en tu .env
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True
    )

# Instancia global para importar en cualquier parte del sistema
settings = Settings()
