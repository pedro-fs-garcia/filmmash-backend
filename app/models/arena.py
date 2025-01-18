from app.models.movie import Movie
import json
import app.dao.MovieDAO as MovieDAO

class Arena:
    def __init__(self, movie1=None, movie2=None, winner = None):
        self.movie1 = movie1
        self.movie2 = movie2
        self.winner = winner


    def calculate_new_scores(self):
        if self.winner == None:
            return None
        else:
            if self.winner == 1:
                winner = self.movie1
                loser = self.movie2
            elif self.winner == 2:
                winner = self.movie2
                loser = self.movie1
            K = 24
            RA = winner.elo
            RB = loser.elo
            EA = 1/(1+10**((RB-RA)/400))
            EB = 1/(1+10**((RA-RB)/400))
            new_RA = RA + K*(1 - EA)
            new_RB = RB + K*(0 - EB)
            winner.elo = int(new_RA)
            loser.elo = int(new_RB)
            return [winner, loser]
    

    def to_json(self):
        tojson = {
            "movie1": {
                "film_id":self.movie1.id,
                "name":self.movie1.title,
                "director":self.movie1.director,
                "year":self.movie1.year,
                "score":self.movie1.elo,
                "poster":self.movie1.poster_url
            },

            "movie2": {
                "film_id":self.movie2.id,
                "name":self.movie2.title,
                "director":self.movie2.director,
                "year":self.movie2.year,
                "score":self.movie2.elo,
                "poster":self.movie2.poster_url
            }
        }
        return json.dumps(tojson)


def build_arena():
    movies = MovieDAO.get_two_random_movies()
    return Arena(movies[0], movies[1], None)


def set_arena_from_post(json_dict: dict):
    movie1_id = int(json_dict.get("movie1"))
    movie2_id = int(json_dict.get("movie2"))
    new_arena = Arena()
    new_arena.movie1 = MovieDAO.get_movie_by_id(movie1_id)
    new_arena.movie2 = MovieDAO.get_movie_by_id(movie2_id)
    winner = json_dict.get("winner")
    if winner == movie1_id: new_arena.winner = 1
    elif winner == movie2_id: new_arena.winner = 2
    return new_arena


def save_new_scores(arena:Arena):
    movies = arena.calculate_new_scores()
    MovieDAO.update_scores(movies[0], movies[1])