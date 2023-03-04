from fastapi import APIRouter
from fastapi import Path, Query, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from middleware.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()




#get all movies
@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db =Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


#get a movie by id
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movie(id: int=Path(ge=1, le=200)) -> Movie:
    db = Session()
    try:
        result = MovieService(db).get_movie(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    except:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Couldn't find your movie, try another id"})

    
    


#get a movie by category
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])#to diferenciate from movies, just add an "/" at the end of the name
def get_movie_by_category(category: str = Query(min_length=2, max_length=15)) -> List[Movie]:#if I define on the function a parameter but not in the decorator, then automatically is defined as a query request
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


#Create a new movie
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).new_movie(movie)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Movie created successfully!"})


#Modify an existing movie
@movie_router.put('/movies/{id}',  tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_movie(id:int, movie: Movie) ->dict:
    db =Session()
    try:
        MovieService(db).modify_movie(id, movie)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Changes saved successfully"})
    except:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Movie doesn't exist, please verify your id"})
    
    

#Delete a movie by id
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_movie(id:int) -> dict:
    db =Session()
    try:
        MovieService(db).delete_movie(id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Movie deleted successfully!"})
    except:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Movie doesn't exist, please verify your id"})
    
    