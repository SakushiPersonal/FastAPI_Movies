from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movie_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def new_movie(self, body: Movie):
        result = MovieModel(**body.dict())
        self.db.add(result)
        self.db.commit()
        return result
    
    def modify_movie(self, id, data:Movie):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        result.title = data.title
        result.overview = data.overview
        result.year = data.year
        result.rating = data.rating
        result.category = data.category
        self.db.commit()
        return result
    
    def delete_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(result)
        self.db.commit()
        return result
    
    
    
    
    
    



    