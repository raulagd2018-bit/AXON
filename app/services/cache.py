# app/services/cache.py
import redis
import json
import logging
import os
from typing import Optional, Any
from bson import ObjectId

logger = logging.getLogger("axioma.cache")

# Helper para serializar tipos complejos (como MongoDB ObjectId)
class AxiomaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

class CacheService:
    def __init__(self):
        self.client = redis.Redis.from_url(
            os.getenv("REDIS_URL", "redis://redis:6379/0"),
            decode_responses=True,
            socket_timeout=2.0,
            socket_connect_timeout=2.0
        )

    def get(self, key: str) -> Optional[Any]:
        try:
            data = self.client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.warning(f"Error de lectura en caché {key}: {e}")
            return None

    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        try:
            serialized_data = json.dumps(value, cls=AxiomaEncoder)
            return self.client.setex(key, expire, serialized_data)
        except Exception as e:
            logger.warning(f"Error de escritura en caché {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.warning(f"Error borrando caché {key}: {e}")
            return False

# Exportamos una instancia única (Singleton)
cache = CacheService()
