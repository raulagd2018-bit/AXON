from .celery_app import celery_app

@celery_app.task(bind=True, max_retries=3)
def process_user_event(self, event_data):
    """
    Procesa un evento del usuario (like, post, búsqueda)
    sin bloquear la interfaz.
    """
    try:
        # Aquí irá la lógica de entrenamiento para tu IA
        # y el cálculo de dopamina.
        print(f"Procesando evento para IA: {event_data}")
        return True
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
