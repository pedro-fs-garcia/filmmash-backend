class Movie:
    def __init__(self, id:str|None, name:str|None, director:str|None, score=1400, poster=None):
        self.id = id
        self._name = name
        self._director = director
        self._score = score
        self._poster = poster
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, director):
        self._director = director

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def poster(self):
        return self._poster

    @poster.setter
    def poster(self, poster):
        self._poster = poster
