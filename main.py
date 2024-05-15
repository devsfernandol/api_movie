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
        
    }
]



@app.get('/', tags=['Home'])

def message():

    return "Hello world"

@app.get('/movies', tags=['Movies'])

def get_movies():
    return movies