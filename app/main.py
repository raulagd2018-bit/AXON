import logging
import sys
import uuid
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

# Importaciones internas
from app.routes import interactions, posts, chat, auth
from app.database import connect_to_mongo, close_mongo_connection
from app.core.config import settings
from app.core.connection import manager, listen_to_redis # Importamos manager y el puente

# 1. Logging Profesional
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - [%(levelname)s] - [ReqID: %(request_id)s] - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    class RequestIDFilter(logging.Filter):
        def filter(self, record):
            if not hasattr(record, "request_id"):
                record.request_id = "INIT"
            return True
    logging.getLogger().addFilter(RequestIDFilter())

setup_logging()
logger = logging.getLogger("axon.core")

# 2. Lifespan: Orquestador del ciclo de vida
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("--- [STARTUP] Inicializando Motores de AXON ---", extra={"request_id": "SYSTEM_INIT"})
    await connect_to_mongo()
    
    # Iniciamos el puente de comunicación con el Worker en background
    task = asyncio.create_task(listen_to_redis(manager))
    logger.info("--- [STARTUP] Puente de Redis activado ---", extra={"request_id": "SYSTEM_INIT"})
    
    yield
    
    # Shutdown
    logger.info("--- [SHUTDOWN] Desconectando Sistemas ---", extra={"request_id": "SYSTEM_SHUTDOWN"})
    task.cancel() # Cancelamos la tarea de fondo al cerrar
    await close_mongo_connection()

# 3. Instanciación Profesional
app = FastAPI(
    title="AXON Core API",
    description="Motor central de IA y Ecosistema de Agentes",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None
)

# 4. Middleware de Trazabilidad
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    # Inyectamos el ID globalmente para los logs de esta petición
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# 5. Seguridad y Monitoreo
Instrumentator().instrument(app).expose(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Global Error Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    req_id = request.headers.get("X-Request-ID", "UNKNOWN")
    logger.error(f"Panic: {str(exc)}", extra={"request_id": req_id})
    return JSONResponse(status_code=500, content={"status": "error", "message": "Fallo crítico en AXON", "request_id": req_id})

# 7. Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(interactions.router, prefix="/api/v1", tags=["Interactions"])
app.include_router(chat.router, prefix="/ws", tags=["Chat"])

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "online", "system": "AXON_CORE_V1"}
