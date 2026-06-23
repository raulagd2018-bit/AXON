# app/models/interaction.py
from pydantic import BaseModel

class InteractionSchema(BaseModel):
    user_id: str
    action_type: str  # ej: "like", "view", "comment"
    target_id: str
