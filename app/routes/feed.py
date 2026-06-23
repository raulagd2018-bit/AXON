# app/routes/feed.py
from fastapi import APIRouter
from ..services.recommendation import get_personalized_feed

router = APIRouter()

@router.get("/my-feed/{user_id}")
async def get_feed(user_id: str):
    feed = await get_personalized_feed(user_id)
    return {"status": "success", "data": feed}
