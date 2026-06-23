import time
import functools
import structlog

logger = structlog.get_logger()

def track_efficiency(task_name: str):
    """
    Decorador para medir el tiempo de ejecución de cualquier función de agente.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            duration = time.perf_counter() - start
            
            # Aquí inyectamos la métrica en los logs estructurados
            logger.info("task_completed", 
                        task=task_name, 
                        duration_seconds=round(duration, 4),
                        status="success")
            return result
        return wrapper
    return decorator
