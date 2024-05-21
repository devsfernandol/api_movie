from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app=FastAPI()
app.title="FastAPI Para Peliculas"
app.version="0.0"


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

def create_movies(id: int = Body(), title: str = Body(), overview:str = Body(), year:int = Body(), rating: float = Body(), category: str = Body()):

    movies.append(
        {"id":id,
         "title":title,
         "overview":overview,
         "year":year,
         "rating":rating,
         "category":category
         }
    )

    return movies


@app.put ('/movies/{id}', tags=['Movies'])

def update_movie(id: int , title: str = Body(), overview:str = Body(), year:int = Body(), rating: float = Body(), category: str = Body()):
    for item in movies:
        if item["id"] == id:
            item['title']= title
            item['overview']= overview
            item['year']= year
            item['rating']= rating
            item['category']= category
            return movies

@app.delete('/movies/{id}', tags=['Movies'])

def delete_movie(id : int):
    for item in movies: 
        if item["id"] == id:
            movies.remove(item)
            return movies