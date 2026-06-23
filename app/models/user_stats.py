# app/models/user_stats.py
from pydantic import BaseModel

class UserStats(BaseModel):
    user_id: str
    dopamine_level: float = 0.0  # Nivel de adicción calculado
    axioma_credits: int = 0      # Puntos de estatus
    total_interactions: int = 0
