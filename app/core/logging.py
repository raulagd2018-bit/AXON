import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer() # Formato ideal para producción
    ]
)
logger = structlog.get_logger()
