from database import configure
import database
import mysql.connector
import json

directors_films = json.load(open("./static/directors_films.json", encoding = "UTF-8"))

def create_table_films():
    try:
        con = mysql.connector.connect(**configure)
        if con.is_connected():
            cur = con.cursor()
            query = "create table films(film_id int auto_increment not null, name varchar(255), director varchar(50), score int, poster varchar(500), primary key(film_id))"
            cur.execute(query)
            con.commit()
            print("table 'films' was successfully created")
    except OSError as e:
        print(f"Erro ao inserir dados no MySQL: {e}")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()



def write_movies(directors_films):
    try:
        con = mysql.connector.connect(**configure)
        if con.is_connected():
            cur = con.cursor()
            query = "INSERT INTO films (name, director, score, poster) VALUES (%s, %s, %s, %s)"
            for diretor, filmes in directors_films.items():
                for filme in filmes:
                    director = diretor.replace("_", " ").title()
                    posterName = f"{filme.replace(' ', '_')}.jpg"
                    posterUrl = "https://raw.githubusercontent.com/pedro-fs-garcia/filmmash-backend/refs/heads/main/app/static/images/" + posterName
                    score = 1400
                    values = (filme.replace("_", " ").capitalize(), director, score, posterUrl)
                    cur.execute(query, values)
                    con.commit()
            print("Filmes inseridos com sucesso.")
    except OSError as e:
        print(f"Erro ao inserir dados no MySQL: {e}")
    finally:
        if cur:
            cur.close()
        if con:
            con.close()

create_table_films()
write_movies(directors_films)