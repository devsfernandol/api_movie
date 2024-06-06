from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.security import HTTPBearer
from config.database import  engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
app=FastAPI()
app.title="FastAPI Para Peliculas"
app.version="0.0"


Base.metadata.create_all(bind=engine)


app.add_middleware(ErrorHandler)
app.include_router(movie_router)



class User(BaseModel):
    email : str
    password: str




movies =[
    
    {

        "id":1,
        "title":"Avatar",
        "overview":"En mundo Extrano",
        "year":"2009",
        "ranting":1.7,
        "category":"Ficcion"
        
    },

        {

        "id":2,
        "title":"Rapido y Furiso",
        "overview":"Brian trata de integrarse a un grupo de corredores iligales",
        "year":"2001",
        "ranting":10,
        "category":"Accion"
        
    }
]



@app.get('/', tags=['Home'])

def message():

    return "Hello world"


@app.post('/login', tags=['auth'])

def login(user:User):

    if user.email=="admin@gmail.com" and user.password=="admin":

        token : str = create_token(user.dict())

        return JSONResponse(status_code=200, content=token)

