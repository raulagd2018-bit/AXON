import logging
import json
import redis
from celery import Celery
from app.core.config import settings

# Ajustamos la URL para asegurar el puerto 6379 de Redis
redis_url = settings.DATABASE_URL.replace("mongodb", "redis").replace("27017", "6379")

celery_app = Celery("axioma_worker", broker=redis_url, backend=redis_url)
redis_client = redis.from_url(redis_url)

logger = logging.getLogger("axon.worker")

@celery_app.task(bind=True, max_retries=3)
def procesar_ia_task(self, user_id: str, prompt: str, session_id: str):
    logger.info(f"Procesando tarea IA: {session_id}")
    try:
        # --- Lógica de IA ---
        resultado = f"AXON IA ha procesado tu solicitud: {prompt}"
        
        # --- Notificación mediante Redis Pub/Sub ---
        # Enviamos el mensaje a un canal que FastAPI estará escuchando
        payload = {
            "user_id": user_id,
            "content": resultado,
            "session_id": session_id
        }
        redis_client.publish("chat_updates", json.dumps(payload))
        
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error crítico: {str(e)}")
        raise self.retry(exc=e, countdown=5)
