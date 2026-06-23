from celery import Celery
import os

# Configuración del broker (Redis)
# Usamos una variable de entorno para seguridad extrema
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "axioma_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Configuración de optimización para alta carga
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_acks_late=True, # Garantiza que no se pierdan tareas si el worker falla
    worker_prefetch_multiplier=1 # Ajustado para precisión en tareas pesadas
)
