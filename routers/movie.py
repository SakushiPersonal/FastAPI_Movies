from fastapi import APIRouter
from fastapi import Path, Query, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from middleware.jwt_bearer import JWTBearer

movie_router = APIRouter()

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


#get all movies
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db =Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


#get a movie by id
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movie(id: int=Path(ge=1, le=200)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Couldn't find your movie, try another id"})

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    


#get a movie by category
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])#to diferenciate from movies, just add an "/" at the end of the name
def get_movie_by_category(category: str = Query(min_length=2, max_length=15)) -> List[Movie]:#if I define on the function a parameter but not in the decorator, then automatically is defined as a query request
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


#Create a new movie
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie) -> dict:
    # Paso 1
    db = Session()
   # Paso 2
    new_movie = MovieModel(**movie.dict())
   # Paso 3
    db.add(new_movie)
  # Paso 4
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Movie created successfully!"})


#Modify an existing movie
@movie_router.put('/movies/{id}',  tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_movie(id:int, movie: Movie) ->dict:
    db =Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Movie doesn't exist, please verify your id"})
    
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Changes saved successfully"})
    
    


#Delete a movie by id
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_movie(id:int) -> dict:
    db =Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Movie doesn't exist, please verify your id"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Movie deleted successfully!"})