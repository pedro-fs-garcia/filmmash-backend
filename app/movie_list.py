from movie import Movie
import database
import json

class Movie_list:    
    def __init__(self):
        self.movie_list = database.build_movie_list()
    
    def to_json(self):
        list_all = self.movie_list
        tojson = {}
        for movie in self.movie_list:
            tojson[movie.id] = {"name": movie.name, "director":movie.director, "score":movie.score, "poster":movie.poster}    
        print(tojson)
        return json.dumps(tojson)