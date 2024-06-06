from fastapi import APIRouter
from fastapi import   Request,  Depends
from fastapi.responses import  JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field ,  conint, confloat
from typing import Coroutine, Optional, List
from fastapi.security import HTTPBearer
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer


movie_router = APIRouter()

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
        



@movie_router.get('/movies', tags=['Movies'], response_model=list[Movie], status_code=200, dependencies=[Depends(JWTBearer())])

def get_movies() -> list[Movie]:
    db= Session()
    result = db.query(MovieModel).all()

    return JSONResponse(status_code=200 ,content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie)

def get_movie(id:int) -> Movie:

    db= Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        return JSONResponse(status_code=200, content={'message':"No Existe"})
    
        
    return JSONResponse(status_code=404,content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['Movies'], response_model=list[Movie], status_code=200)

def get_movies_category(category:str) -> list[Movie]:

    db = Session()
    result= db.query(MovieModel).filter(MovieModel.category == category).all()

    if not result:
        return JSONResponse( status_code=200 , content={'message':"NO hay una pelicula con esa categoria"})

    
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@movie_router.post('/movies/', tags=['Movies'], response_model=dict, status_code=201)

def create_movies(movie : Movie) -> dict:

    db= Session()
    new_movie = MovieModel(**movie.model_dump())

    db.add(new_movie)

    db.commit()
    

    return JSONResponse(status_code=201,content={"message":"Se ha agreado la pelicula"})


@movie_router.put ('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)

def update_movie(id: int , movie:Movie) -> dict:

    db= Session()
    result= db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=200, content={'message':"No Existe"})
    
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category

    db.commit()
    return JSONResponse(status_code=200,content={"message":"Se ha Actulizado la Pelicula"})

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)

def delete_movie(id : int) -> dict:

    db= Session()
    result= db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=200, content={'message':"No Existe"})
    
    db.delete(result)
    db.commit()

 
    return JSONResponse(status_code=201,content={"message":"Se ha eliminado la pelicula"})