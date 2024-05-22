from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field ,  conint, confloat
from typing import Optional 

app=FastAPI()
app.title="FastAPI Para Peliculas"
app.version="0.0"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5 ,max_length=10)
    overview: str = Field(min_length=10 ,max_length=50)
    year: int = Field(le=2024)
    rating: float = Field (le=2)
    category: str =Field (min_length=2 , max_length=5)


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

@app.get('/movies', tags=['Movies'])

def get_movies():
    return movies

@app.get('/movies/{id}', tags=['Movies'])

def get_movie(id:int):
    
    for item in movies:
        if item["id"] == id:
            return item
        
    return []

@app.get('/movies/', tags=['Movies'])

def get_movies_category(category:str, year:int):
    return [item for item in movies if item['category'] == category ]


@app.post('/movies/', tags=['Movies'])

def create_movies(movie : Movie):

    movies.append(movie)

    return movies


@app.put ('/movies/{id}', tags=['Movies'])

def update_movie(id: int , movie:Movie):
    for item in movies:
        if item["id"] == id:
            item['title']= movie.title
            item['overview']= movie.overview
            item['year']= movie.year
            item['rating']= movie.rating
            item['category']= movie.category
            return movies

@app.delete('/movies/{id}', tags=['Movies'])

def delete_movie(id : int):
    for item in movies: 
        if item["id"] == id:
            movies.remove(item)
            return movies