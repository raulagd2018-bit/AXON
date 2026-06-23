from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .security import verify_password, create_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/login")
def login(user_data: dict):
    # Aquí iría tu lógica de búsqueda en MongoDB
    # user = db.users.find_one({"email": user_data['email']})
    
    # Ejemplo de lógica:
    # if not verify_password(user_data['password'], user['hashed_password']):
    #     raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    access_token = create_access_token(data={"sub": user_data['email']})
    return {"access_token": access_token, "token_type": "bearer"}
