# app/routes/interactions.py
import logging
from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from ..models.interaction import InteractionSchema  # Asegúrate de tener este modelo
from ..tasks import process_user_event

router = APIRouter()
logger = logging.getLogger("axioma.interactions")

@router.post(
    "/interact", 
    status_code=status.HTTP_202_ACCEPTED,
    summary="Registra una interacción de usuario",
    description="Encola una interacción para análisis asíncrono y recompensas de dopamina."
)
async def handle_interaction(interaction: InteractionSchema):
    """
    Endpoint de alta velocidad. 
    Acepta el evento y lo delega a la cola (Celery).
    """
    try:
        # Validación: El objeto interaction ya viene validado por Pydantic
        # al definirlo como parámetro.
        
        # Delegar el trabajo pesado a nuestro "Cerebro Asíncrono"
        # .delay() es la magia de Celery para enviar la tarea a Redis
        task = process_user_event.delay(interaction.model_dump())
        
        logger.info(f"Interacción encolada. Task ID: {task.id} | User: {interaction.user_id}")
        
        return {
            "status": "accepted", 
            "task_id": task.id,
            "message": "Event queued for background processing"
        }

    except Exception as e:
        logger.error(f"Error crítico al encolar interacción: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo procesar la interacción en este momento."
        )
