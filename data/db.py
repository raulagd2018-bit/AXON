from motor.motor_asyncio import AsyncIOMotorClient
from config import config

class DatabaseManager:
    def __init__(self):
        # Conexión profesional al contenedor Docker que acabamos de levantar
        self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.client.axioma_db

    async def test_connection(self):
        try:
            await self.db.command("ping")
            return True
        except Exception:
            return False

db = DatabaseManager()
