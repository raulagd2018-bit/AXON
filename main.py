import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator  # Importación profesional
from app.routes import interactions, posts, chat, auth
from app.database import connect_to_mongo, close_mongo_connection
from app.security.rate_limiter import rate_limit_middleware

# Configuración de logs profesional
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("axioma.main")

# 1. Instanciación del Core
app = FastAPI(
    title="Axioma Core",
    description="Motor de IA y Plataforma de Alta Escalabilidad",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 2. Configuración de Monitoreo (Fase 11 - Observabilidad)
# Esto expone automáticamente el endpoint /metrics para Prometheus
Instrumentator().instrument(app).expose(app)

# 3. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Eventos de Ciclo de Vida
@app.on_event("startup")
async def startup():
    logger.info("--- Iniciando Axioma Core (Production Mode) ---")
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    logger.info("--- Apagando Axioma Core ---")
    await close_mongo_connection()

# 5. Escudo de Hierro (Middleware)
app.middleware("http")(rate_limit_middleware)

# 6. Enrutamiento Modular
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(interactions.router, prefix="/api/v1", tags=["Interactions"])
app.include_router(posts.router, prefix="/api/v1", tags=["Posts"])
app.include_router(chat.router, prefix="/ws", tags=["Chat"])

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "Axioma Core Operativo",
        "version": "1.0.0",
        "environment": "production"
    }

