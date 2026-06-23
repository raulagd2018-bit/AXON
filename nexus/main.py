import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Header, Depends
from pydantic import BaseModel, Field
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config
from data.db import db
from nexus.oracle_service import oracle
from nexus.security import verify_token

@asynccontextmanager
async def lifespan(app: FastAPI):
    if await db.test_connection():
        print("--- [NEXUS] Conexión a MongoDB establecida ---")
    else:
        print("--- [NEXUS] AVISO: Fallo en conexión a MongoDB ---")
    yield
    print("--- [NEXUS] Cerrando servicios ---")

app = FastAPI(title="Axioma Nexus Core", version=config.VERSION, lifespan=lifespan)

class RequestModel(BaseModel):
    user_id: str
    action: str
    payload: dict = Field(default_factory=dict)

async def get_token_header(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Falta token Bearer")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    return payload

@app.post("/v1/orchestrate", status_code=status.HTTP_202_ACCEPTED)
async def orchestrate(data: RequestModel, auth: dict = Depends(get_token_header)):
    try:
        await db.db.logs.insert_one({"user_id": data.user_id, "action": data.action})
        response_data = {"status": "success"}
        if data.action == "search":
            response_data["oracle_result"] = await oracle.process_search(data.payload.get("query", ""))
        
        return {"status": "completed", "routing": data.action, "response": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error crítico")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
