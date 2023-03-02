from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "First FastAPI App " #Here we select the title of our App
app.version = "0.0.5" #Here we can indicate our actual app version 

movies = [
    {
    "id": 1,
    "title": "Secret Room",
    "overview": "All our secrets together in this room",
    "year": "2069",
    "rating": 8.9,
    "category": "+18"
    },
    {
    "id": 2,
    "title": "Secret Room 2",
    "overview": "All our secrets together in this room at the sorrow night",
    "year": "2169",
    "rating": 6.8,
    "category": "++18"
    }
]

@app.get('/', tags=['home'])#With tags we can separate our diferents routes by name to identify them easily.
def message():
    return HTMLResponse('<h1>Hello world!</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return []

@app.get('/movies/', tags=['movies'])#to diferenciate from movies, just add an "/" at the end of the name
def get_movie_by_category(category: str):#if I define on the function a parameter but not in the decorator, then automatically is defined as a query request
    movie = list(filter(lambda movie: movie["category"] == category, movies))
    return movie

@app.post('/movies', tags=['movies'])
def create_movie(id:int=Body(), title:str=Body(), overview:str=Body(), year:str=Body(), rating:int=Body(), category:str=Body()):
    movies.append(
        {
        "id":id,
        "title":title,
        "overview":overview,
        "year":year,
        "rating":rating,
        "category":category
        }
    )

    return movies
