import logging
import json
import asyncio
import redis.asyncio as aioredis
from fastapi import WebSocket
from typing import Dict

logger = logging.getLogger("axon.core.connection")

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"[CONNECTION] Usuario conectado: {user_id}. Total: {len(self.active_connections)}")

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"[DISCONNECT] Usuario desconectado: {user_id}")

    async def send_json(self, user_id: str, message: dict):
        connection = self.active_connections.get(user_id)
        if connection:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"[ERROR] Fallo al enviar a {user_id}: {str(e)}")
                self.disconnect(user_id)
        else:
            logger.warning(f"[WARN] Intento de envío a usuario no conectado: {user_id}")

    async def broadcast(self, message: dict):
        for user_id, connection in list(self.active_connections.items()):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(user_id)

# --- ESCUCHA DE EVENTOS (PUENTE CON EL WORKER) ---
async def listen_to_redis(manager: ConnectionManager):
    """
    Este loop se ejecutará en background. 
    Escucha eventos publicados por el Worker en Redis.
    """
    redis = aioredis.from_url("redis://localhost:6379/0")
    pubsub = redis.pubsub()
    await pubsub.subscribe("chat_updates")
    
    logger.info("[REDIS] Puente de comunicación establecido.")
    
    async for message in pubsub.listen():
        if message["type"] == "message":
            try:
                data = json.loads(message["data"])
                # Enviamos el mensaje al usuario destino
                await manager.send_json(data["user_id"], {
                    "type": "ai_response",
                    "content": data["content"],
                    "session_id": data["session_id"]
                })
            except Exception as e:
                logger.error(f"[REDIS] Error procesando mensaje: {e}")

# Instancia única (Singleton)
manager = ConnectionManager()
