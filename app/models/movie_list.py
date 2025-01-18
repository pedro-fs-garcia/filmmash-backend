from app.models.movie import Movie
import app.dao.MovieDAO as MovieDAO
import json

class Movie_list:    
    def __init__(self):
        self.movie_list = MovieDAO.build_movie_list()
    
    def to_json(self):
        list_all = self.movie_list
        tojson = {}
        for movie in self.movie_list:
            tojson[movie.id] = {"name": movie.title, "director":movie.director, "year":movie.year,"score":movie.elo, "poster":movie.poster_url}    
        print(tojson)
        return json.dumps(tojson)