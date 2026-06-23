import uuid
from fastapi import Request

async def trace_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    # Inyectamos el ID en el contexto de log
    logger = structlog.get_logger().bind(request_id=request_id)
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
