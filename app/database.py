import mysql.connector
import sys
import config
import json
from movie import Movie

configure = {"user": f"{config.DB_USER}", "password": f"{config.DB_PASSWORD}", "host": f"{config.DB_HOST}", "database": f"{config.DB_NAME}"}



def update_scores(winner: Movie, loser: Movie):
    try:
        con = mysql.connector.connect(**configure)
        if con.is_connected():
            cur = con.cursor()
            query = "UPDATE films SET score = %s WHERE film_id = %s"
            cur.execute(query, (winner.score, winner.id))
            cur.execute(query, (loser.score, loser.id))
            con.commit()
            print("scores were successfully updated")
    except OSError as e:
        print(f"Erro ao inserir dados no MySQL: {e}")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()


def get_two_random_movies():
    try:
        con = mysql.connector.connect(**configure)
        if con.is_connected():
            cur = con.cursor()
            query = "SELECT * FROM films ORDER BY RAND() LIMIT 2"
            cur.execute(query)
            res = cur.fetchall()
    except OSError as e:
        print(f"Erro ao inserir dados no MySQL: {e}")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
    movies = []
    for i in res:
        id = i[0]
        name = i[1]
        director = i[2]
        score = i[3]
        poster = i[4]
        movies.append(Movie(id, name, director, score, poster))
    return movies

def get_all_movies():
    try:
        con = mysql.connector.connect(**configure)
        if con.is_connected():
            cur = con.cursor()
            query = "SELECT * FROM films ORDER BY score DESC, film_id"
            cur.execute(query)
            res = cur.fetchall()
            print("movies were successfully fetched")
    except OSError as e:
        print(f"Erro ao acessar dados no MySQL: {e}")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
    return res


def build_movie_list():
    movie_list = []
    movies_data = get_all_movies()
    position = 1
    for movie_tuple in movies_data:
        movie = Movie(position, movie_tuple[1], movie_tuple[2], movie_tuple[3], movie_tuple[4])
        movie_list.append(movie)
        position += 1
    return movie_list


def get_movie_by_id(movie_id:int) -> Movie :
    try:
        con = mysql.connector.connect(**configure)
        if con.is_connected():
            cur = con.cursor()
            query = "SELECT film_id, name, director, score, poster FROM films WHERE film_id = %s"
            cur.execute(query, (movie_id,))
            res = cur.fetchall()
    except OSError as e:
        print(f"Erro ao inserir dados no MySQL: {e}")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
    if len(res) > 0:
        res = res[0]
        movie = Movie(res[0], res[1], res[2], res[3], res[4])
        return movie
    return None
