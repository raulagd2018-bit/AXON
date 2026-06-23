# app/models/post.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PostSchema(BaseModel):
    id: Optional[str] = None
    user_id: str
    content_url: str
    caption: str
    content_type: str = "video"  # 'video' o 'image'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Metadatos para la IA (Dopamina/Engagement)
    engagement_score: float = 0.0
    tags: List[str] = []

    class Config:
        json_encoders = {ObjectId: str}
