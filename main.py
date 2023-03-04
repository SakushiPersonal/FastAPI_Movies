from fastapi import FastAPI, Body, Path, Query, status, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie

app = FastAPI()
app.title = "First FastAPI App " #Here we select the title of our App
app.version = "0.0.5" #Here we can indicate our actual app version 


Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials! >:c ")
        

class User(BaseModel):
    email:str
    password:str


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

'''Not really nedded JsonResponse because FastAPI return by default in that format, is just nedded in a specific moments '''


#home
@app.get('/', tags=['home'], status_code=status.HTTP_200_OK)#With tags we can separate our diferents routes by name to identify them easily.
def message():
    return HTMLResponse(status_code=status.HTTP_200_OK, content='<h1>Hello world!</h1>')


#get all movies
@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=status.HTTP_200_OK, content=movies)


#get a movie by id
@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=status.HTTP_200_OK)
def get_movie(id: int=Path(ge=1, le=200)) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(status_code=status.HTTP_200_OK, content=movie)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Couldn't find your movie, try another id"})


#get a movie by category
@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK)#to diferenciate from movies, just add an "/" at the end of the name
def get_movie_by_category(category: str = Query(min_length=4, max_length=15)) -> List[Movie]:#if I define on the function a parameter but not in the decorator, then automatically is defined as a query request
    movie = list(filter(lambda movie: movie["category"] == category, movies))
    return JSONResponse(status_code=status.HTTP_200_OK, content=movie)


#Create a new movie
@app.post('/movies', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Movie created successfully!"})


#Modify an existing movie
@app.put('/movies/{id}',  tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id:int, movie: Movie) ->dict:
    for mov in movies:
        if mov["id"] == id:
            mov["title"] = movie.title
            mov["overview"] = movie.overview
            mov["year"] = movie.year
            mov["rating"] = movie.rating
            mov["category"] = movie.category

            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Changes saved successfully"})
    
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Movie doesn't exist, please verify your id"})


#Delete a movie by id
@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def delete_movie(id:int) -> dict:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Movie deleted successfully!"})
        
@app.post('/login', tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.dict())
    return JSONResponse(status_code=status.HTTP_200_OK, content=token)