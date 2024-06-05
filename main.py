from fastapi import FastAPI, Body, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field ,  conint, confloat
from typing import Coroutine, Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app=FastAPI()
app.title="FastAPI Para Peliculas"
app.version="0.0"


Base.metadata.create_all(bind=engine)


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data =validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales Invalidas")


class User(BaseModel):
    email : str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5 ,max_length=30)
    overview: str = Field(min_length=5 ,max_length=100)
    year: int = Field(le=2024)
    rating: float = Field ()
    category: str =Field (min_length=2 , max_length=30)


    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Titulo",
                "overview": "descripcion",
                "year": 2022,
                "rating": 1.5,
                "category": "Accion"
            }
        }
        




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

@app.get('/movies', tags=['Movies'], response_model=list[Movie], status_code=200, dependencies=[Depends(JWTBearer())])

def get_movies() -> list[Movie]:
    db= Session()
    result = db.query(MovieModel).all()

    return JSONResponse(status_code=200 ,content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie)

def get_movie(id:int) -> Movie:
    
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
        
    return JSONResponse(status_code=404,content=[])

@app.get('/movies/', tags=['Movies'], response_model=list[Movie], status_code=200)

def get_movies_category(category:str) -> list[Movie]:
    
    data= [item for item in movies if item['category'] == category ]
    
    return JSONResponse(status_code=200,content=data)


@app.post('/movies/', tags=['Movies'], response_model=dict, status_code=201)

def create_movies(movie : Movie) -> dict:

    db= Session()
    new_movie = MovieModel(**movie.model_dump())

    db.add(new_movie)

    db.commit()
    

    return JSONResponse(status_code=201,content={"message":"Se ha agreado la pelicula"})


@app.put ('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)

def update_movie(id: int , movie:Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item['title']= movie.title
            item['overview']= movie.overview
            item['year']= movie.year
            item['rating']= movie.rating
            item['category']= movie.category
            return JSONResponse(status_code=200,content={"message":"Se ha Actulizado la Pelicula"})

@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)

def delete_movie(id : int) -> dict:
    for item in movies: 
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=201,content={"message":"Se ha eliminado la pelicula"})