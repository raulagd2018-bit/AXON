# app/security/rate_limiter.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from ..services.cache import cache
import logging

# Configuración
LIMIT = 100
WINDOW = 60  # Segundos

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Excluimos rutas de monitoreo o métricas si es necesario
        if request.url.path in ["/metrics", "/health"]:
            return await call_next(request)

        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        redis_conn = cache.client

        try:
            # Lógica atómica: INCR y EXPIRE (si es nuevo)
            pipe = redis_conn.pipeline()
            pipe.incr(key)
            pipe.ttl(key)
            results = pipe.execute()

            current_count = results[0]
            ttl = results[1]

            if ttl == -1:
                redis_conn.expire(key, WINDOW)

            # Validación de límite
            if current_count > LIMIT:
                logger.warning(f"Rate limit excedido para IP: {client_ip}")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Demasiadas peticiones. Por favor, espera un momento."},
                )

        except Exception as e:
            # Fail-open: Si Redis cae, no bloqueamos la API, pero logueamos el error
            logger.error(f"Error en Rate Limiter: {e}")
            return await call_next(request)

        # Si todo está bien, continuamos
        return await call_next(request)
