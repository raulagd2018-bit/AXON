# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))

async def close_mongo_connection():
    db.client.close()
