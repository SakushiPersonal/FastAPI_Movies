from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = "First FastAPI App " #Here we select the title of our App
app.version = "0.0.5" #Here we can indicate our actual app version 

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=4, max_length=20)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le =10.0)
    category: str = Field(min_length=3, max_length=10)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My movie",
                "overview": "movie description",
                "year": "2023",
                "rating": 10.0,
                "category": "+18"
            }
        }

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
def get_movie(id: int=Path(ge=1, le=200)):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return []

@app.get('/movies/', tags=['movies'])#to diferenciate from movies, just add an "/" at the end of the name
def get_movie_by_category(category: str = Query(min_length=4, max_length=15)):#if I define on the function a parameter but not in the decorator, then automatically is defined as a query request
    movie = list(filter(lambda movie: movie["category"] == category, movies))
    return movie

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)

    return movies


@app.put('/movies/{id}',  tags=['movies'])
def update_movie(id:int, movie: Movie):
    for mov in movies:
        if mov["id"] == id:
            mov["title"] = movie.title
            mov["overview"] = movie.overview
            mov["year"] = movie.year
            mov["rating"] = movie.rating
            mov["category"] = movie.category

            return movies
    

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id:int):
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return movies