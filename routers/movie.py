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
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()





@movie_router.get('/movies', tags=['Movies'], response_model=list[Movie], status_code=200,  )

def get_movies() -> list[Movie]:
    db= Session()
    result = MovieService(db).get_movies_all()

    return JSONResponse(status_code=200 ,content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie)

def get_movie(id:int) -> Movie:

    db= Session()
    result = MovieService(db).get_movies(id)

    if not result:
        return JSONResponse(status_code=200, content={'message':"No Existe"})
    
        
    return JSONResponse(status_code=404,content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['Movies'], response_model=list[Movie], status_code=200)

def get_movies_category(category:str) -> list[Movie]:

    db = Session()
    result= MovieService(db).get_movies_category(category)

    if not result:
        return JSONResponse( status_code=200 , content={'message':"NO hay una pelicula con esa categoria"})

    
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@movie_router.post('/movies/', tags=['Movies'], response_model=dict, status_code=201)

def create_movies(movie : Movie) -> dict:

    db= Session()

    MovieService(db).create_movie(movie)

    

    return JSONResponse(status_code=201,content={"message":"Se ha agreado la pelicula"})


@movie_router.put ('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)

def update_movie(id: int , movie:Movie) -> dict:

    db= Session()
    result= MovieService(db).get_movies(id)
    if not result:
        return JSONResponse(status_code=200, content={'message':"No Existe"})
    
    MovieService(db).update_movie(id, movie )
    

    return JSONResponse(status_code=200,content={"message":"Se ha Actulizado la Pelicula"})

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)

def delete_movie(id : int) -> dict:

    db= Session()
    result= MovieService(db).get_movies(id)
    if not result:
        return JSONResponse(status_code=200, content={'message':"No Existe"})
    
    MovieService(db).delete_movie(id)
    
    
 
    return JSONResponse(status_code=201,content={"message":"Se ha eliminado la pelicula"})