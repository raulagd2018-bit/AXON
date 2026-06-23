from fastapi import APIRouter, status, Response
from app.database import db # Tu instancia de conexión a Mongo

router = APIRouter()

@router.get("/ready", tags=["System"])
async def readiness_check():
    # Verifica si la base de datos responde
    try:
        await db.command("ping")
        return {"status": "ready"}
    except Exception:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
