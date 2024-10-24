from movie import Movie
import json
import database

class Arena:
    def __init__(self, movie1 = None, movie2 = None, winner = None):
        self._movie1 = movie1
        self._movie2 = movie2
        self._winner = winner

    @property
    def movie1(self):
        return self._movie1
    
    @movie1.setter
    def movie1(self, movie1:Movie):
        self._movie1 = movie1
    
    @property
    def movie2(self):
        return self._movie2
    
    @movie2.setter
    def movie2(self, movie2:Movie):
        self._movie2 = movie2

    @property
    def winner(self):
        return self._winner
    
    @winner.setter
    def winner(self, winner:int):
        self._winner = winner

    def calculate_new_scores(self):
        if self.winner == None:
            return None
        else:
            if self._winner == 1:
                winner = self._movie1
                loser = self._movie2
            elif self._winner == 2:
                winner = self._movie2
                loser = self._movie1
            K = 24
            RA = winner.score
            RB = loser.score
            EA = 1/(1+10**((RB-RA)/400))
            EB = 1/(1+10**((RA-RB)/400))
            new_RA = RA + K*(1 - EA)
            new_RB = RB + K*(0 - EB)
            winner.score = int(new_RA)
            loser.score = int(new_RB)
            return [winner, loser]
    
    def to_json(self):
        tojson = {
            "movie1": {
                "film_id":self.movie1.id,
                "name":self.movie1.name,
                "director":self.movie1.director,
                "score":self.movie1.score,
                "poster":self.movie1.poster
            },

            "movie2": {
                "film_id":self.movie2.id,
                "name":self.movie2.name,
                "director":self.movie2.director,
                "score":self.movie2.score,
                "poster":self.movie2.poster
            }
        }
        return json.dumps(tojson)


def build_arena():
    movies = database.get_two_random_movies()
    return Arena(movies[0], movies[1], None)


def set_arena_from_post(json_dict: dict):
    movie1_id = int(json_dict.get("movie1"))
    movie2_id = int(json_dict.get("movie2"))
    new_arena = Arena()
    new_arena.movie1 = database.get_movie_by_id(movie1_id)
    new_arena.movie2 = database.get_movie_by_id(movie2_id)
    winner = json_dict.get("winner")
    if winner == movie1_id: new_arena.winner = 1
    elif winner == movie2_id: new_arena.winner = 2
    return new_arena


def save_new_scores(arena:Arena):
    movies = arena.calculate_new_scores()
    database.update_scores(movies[0], movies[1])