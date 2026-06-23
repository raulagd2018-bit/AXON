# app/services/rewards.py
import logging
from ..database import db
from pymongo.errors import PyMongoError

# Configuramos un logger profesional para esta parte del sistema
logger = logging.getLogger("axioma.rewards")

async def add_dopamine_points(user_id: str, points: int) -> bool:
    """
    Actualiza los puntos de dopamina y el conteo de interacciones del usuario.
    Retorna True si la operación fue exitosa, False en caso contrario.
    """
    try:
        # Validación básica de datos
        if not user_id or points <= 0:
            logger.warning(f"Intento de recompensa inválido: user={user_id}, pts={points}")
            return False

        # Operación atómica de actualización
        result = await db.client.axioma.users.update_one(
            {"user_id": user_id},
            {
                "$inc": {
                    "axioma_credits": points, 
                    "total_interactions": 1
                },
                "$set": {"last_interaction": "now"} # Opcional: marca de tiempo de actividad
            },
            upsert=True
        )
        
        logger.info(f"Éxito: Usuario {user_id} recompensado con {points} pts.")
        return result.acknowledged

    except PyMongoError as e:
        # Aquí es donde capturamos errores de base de datos sin tumbar la app
        logger.error(f"Error crítico en base de datos al recompensar usuario {user_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado en rewards service: {e}")
        return False
