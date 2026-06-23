# app/tasks.py
import logging
import asyncio
from celery import Celery
from .services.rewards import add_dopamine_points
import os

# Configuración del logger
logger = logging.getLogger("axioma.tasks")

# Configuración del motor de tareas con configuración de Redis optimizada
celery_app = Celery(
    "axioma_tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

# Diccionario de pesos de dopamina por acción
DOPAMINE_WEIGHTS = {
    "new_post": 20,
    "like": 5,
    "comment": 10,
    "share": 15
}

@celery_app.task(
    bind=True, 
    max_retries=3, 
    default_retry_delay=5,
    name="tasks.process_user_event"
)
def process_user_event(self, event_data: dict):
    """
    Motor de procesamiento asíncrono con distinción de pesos según acción.
    """
    user_id = event_data.get("user_id")
    action = event_data.get("action", "default")
    
    # 1. Validación de integridad
    if not user_id:
        logger.error("Tarea recibida sin user_id. Abortando.")
        return {"status": "error", "message": "Missing user_id"}

    # 2. Selección de recompensa (Dopamina inteligente)
    points = DOPAMINE_WEIGHTS.get(action, 2) # Por defecto 2 puntos

    try:
        # 3. Ejecución profesional del loop asíncrono
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        success = loop.run_until_complete(add_dopamine_points(user_id, points))
        loop.close()

        if not success:
            logger.warning(f"Recompensa fallida para {user_id}. Reintentando...")
            raise Exception("Rewards service returned False")

        logger.info(f"Dopamina entregada: {points} pts a {user_id} por accion: {action}")
        return {"status": "success", "user_id": user_id, "points": points}

    except Exception as exc:
        logger.error(f"Error crítico en proceso de evento para {user_id}: {exc}")
        # Reintento con backoff exponencial implícito en Celery
        raise self.retry(exc=exc)
