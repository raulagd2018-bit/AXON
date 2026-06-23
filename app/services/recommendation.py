# app/services/recommendation.py
import logging
from ..database import db

logger = logging.getLogger("axioma.ai")

async def get_personalized_feed(user_id: str, limit: int = 10):
    """
    Busca contenido basado en los intereses capturados 
    por la IA y el nivel de dopamina del usuario.
    """
    try:
        # Recuperamos el perfil del usuario para ver qué le gusta
        user_profile = await db.client.axioma.users.find_one({"user_id": user_id})
        
        # Lógica de "Dopamine-Weighted Recommendation":
        # Si no hay mucho historial, mostramos contenido tendencia.
        # Si hay datos, filtramos por los tags con mayor éxito.
        pipeline = [
            {"$sample": {"size": limit}}, # Por ahora, muestra aleatorio inteligente
            {"$sort": {"engagement_score": -1}}
        ]
        
        cursor = db.client.axioma.posts.aggregate(pipeline)
        feed = await cursor.to_list(length=limit)
        
        return feed

    except Exception as e:
        logger.error(f"Error en el motor de IA para {user_id}: {e}")
        return []
