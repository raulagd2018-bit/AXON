# app/routes/posts.py
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from ..models.post import PostSchema
from ..database import db
from ..tasks import process_user_event
from ..security.deps import get_current_user
from ..services.cache import cache  # Importamos el Singleton profesional

router = APIRouter()
logger = logging.getLogger("axioma.posts")

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Crea un post",
    description="Persiste un post en MongoDB, actualiza el caché y dispara tareas asíncronas."
)
async def create_post(
    post: PostSchema,
    current_user: str = Depends(get_current_user)
):
    try:
        # 1. Preparación
        post_data = post.model_dump(exclude={"id"})
        post_data["author"] = current_user

        # 2. Persistencia
        result = await db.client.axioma.posts.insert_one(post_data)
        post_id = str(result.inserted_id)
        
        # Insertamos el ID en el diccionario para el caché
        post_data["_id"] = post_id

        # 3. Caché profesional
        cache.set(f"post:{post_id}", post_data)

        # 4. Tarea asíncrona (Celery)
        process_user_event.delay({
            "action": "new_post",
            "post_id": post_id,
            "user_id": current_user
        })

        logger.info(f"Post {post_id} creado correctamente.")
        return {"status": "success", "post_id": post_id}

    except Exception as e:
        logger.error(f"Error crítico al crear post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error procesando la solicitud."
        )

@router.get("/{post_id}")
async def get_post(post_id: str):
    """Estrategia de Caché-Aside para alta disponibilidad."""
    
    # 1. Intentar leer del Singleton 'cache'
    cached_post = cache.get(f"post:{post_id}")
    if cached_post:
        return {"data": cached_post, "source": "cache"}

    # 2. Leer de MongoDB
    try:
        post = await db.client.axioma.posts.find_one({"_id": ObjectId(post_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")

    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    # 3. Normalización y Caching
    post["_id"] = str(post["_id"])
    cache.set(f"post:{post_id}", post)
    
    return {"data": post, "source": "database"}
