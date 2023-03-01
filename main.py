from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "First FastAPI App " #Here we select the title of our App
app.version = "0.0.2" #Here we can indicate our actual app version 

movies = [
    {
    "id": 1,
    "title": "Secret Room",
    "overview": "All our secrets together in this room",
    "year": "2069",
    "rating": 8.9,
    "category": "+18"
    }
]

@app.get('/', tags=['home'])#With tags we can separate our diferents routes by name to identify them easily.
def message():
    return HTMLResponse('<h1>Hello world!</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies