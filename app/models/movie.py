class Movie:
    def __init__(self, id:int, title:str|None, director:str|None, year:int|None, poster_url:str|None, elo=1400):
        self.id = id
        self.title = title
        self.director = director
        self.year = year
        self.poster_url = poster_url
        self.elo = elo


    def __repr__(self):
        return f"<Movie(id={self.id}, title={self.title}, director={self.director}, year={self.year}, poster_url={self.poster_url}, elo={self.elo})>"


