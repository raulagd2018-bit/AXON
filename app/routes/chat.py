import logging
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from app.core.connection import manager
from app.worker import procesar_ia_task

logger = logging.getLogger("axon.chat")
router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    # Generamos un ID de sesión para rastrear esta conexión específica
    session_id = str(uuid.uuid4())
    await manager.connect(websocket, user_id)
    
    logger.info(f"Socket iniciado", extra={"user_id": user_id, "session_id": session_id})
    
    try:
        while True:
            # Recibimos el payload
            data = await websocket.receive_json()
            text = data.get("text")
            
            if not text:
                continue

            # Feedback de estado profesional
            await manager.send_json(user_id, {
                "status": "processing",
                "message": "AXON está procesando tu solicitud...",
                "session_id": session_id
            })

            # Delegación al Worker (Asíncrono)
            # Pasamos el session_id para poder rastrear la respuesta del worker
            procesar_ia_task.delay(user_id, text, session_id)

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        logger.info(f"Usuario desconectado", extra={"user_id": user_id})
    except Exception as e:
        logger.error(f"Error crítico en WebSocket: {str(e)}", extra={"user_id": user_id})
        manager.disconnect(user_id)
