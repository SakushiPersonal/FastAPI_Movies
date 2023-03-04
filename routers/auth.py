from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token




auth_router = APIRouter()

class User(BaseModel):
    email:str
    password:str

@auth_router.post('/login', tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.dict())
    return JSONResponse(status_code=status.HTTP_200_OK, content=token)