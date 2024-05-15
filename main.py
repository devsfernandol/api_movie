from fastapi import FastAPI
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