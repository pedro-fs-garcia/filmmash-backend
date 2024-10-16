import mysql.connector
import sys
import config
import json
from arena import Arena
from movie import Movie

configure = {"user": f"{config.DB_USER}", "password": f"{config.DB_PASSWORD}", "host": f"{config.DB_HOST}", "database": f"{config.DB_NAME}"}


def build_arena():
    movies = get_two_random_movies()
    return Arena(movies[0], movies[1], None)


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


def save_new_scores(arena: Arena):
    movies = arena.calculate_new_scores()
    update_scores(movies[0], movies[1])


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