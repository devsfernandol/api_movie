from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from schemas.user import User






usuario_router = APIRouter()




@usuario_router.post('/login', tags=['auth'])

def login(user:User):

    if user.email=="admin@gmail.com" and user.password=="admin":

        token : str = create_token(user.dict())

        return JSONResponse(status_code=200, content=token)
