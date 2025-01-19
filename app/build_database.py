from mysql.connector import connect, Error
import requests
from app import config
from app.models.movie import Movie
from app.utils.logging_config import app_logger, error_logger

configure = {
    "user": f"{config.DB_USER}", 
    "password": f"{config.DB_PASSWORD}", 
    "host": f"{config.DB_HOST}", 
    "database": f"{config.DB_NAME}",
    "port": f"{config.DB_PORT}"
    }


create_tables_script = """
                    CREATE TABLE IF NOT EXISTS movies (
                    id INT NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    director VARCHAR(50),
                    year INT,
                    poster_url VARCHAR(500),
                    elo INT NOT NULL,
                    PRIMARY KEY (id)
                    );
                """


from dotenv import load_dotenv
import os

load_dotenv()

# Configurações
API_KEY = os.getenv("API_KEY")
API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"


def create_database_if_not_exists():
    try:
        conn = connect(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
        )
        conn.autocommit = True

        with conn.cursor() as cur:
            query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s"
            database_name = configure["database"]
            cur.execute(query, (database_name,))
            if cur.fetchone():
                app_logger.info(f"Database {database_name} already exists")
                return False
            else:
                cur.execute(f"CREATE DATABASE {database_name}")
                app_logger.info(f"Database {database_name} was created.")
                return True
    except Error as e:
        error_logger.error(f"Erro ao criar o banco de dados {configure['database']}: {e}")
        return False
    finally:
        if conn.is_connected():
            conn.close()


def create_tables_if_not_exists(script):
    try:
        conn = connect(**configure)
        with conn.cursor() as cur:
            cur.execute(script)
            app_logger.info("Tables created successfully or already exist.")
        conn.commit() 
        return True
    except Error as e:
        error_logger.error(f"Error when creating tables: {e}")
        return False
    finally:
        if conn.is_connected():
            conn.close()


def is_table_empty(table_name):
    query = f"SELECT COUNT(*) FROM {table_name}"
    try:
        conn = connect(**configure)
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()
            if result[0] == 0:
                app_logger.info(f"Table '{table_name}' is empty.")
                return True
            else:
                app_logger.info(f"Table '{table_name}' has {result[0]} rows.")
                return False
    except Error as e:
        error_logger.error(f"Error checking if table '{table_name}' is empty: {e}")
        return None
    finally:
        if conn.is_connected():
            conn.close()


# Função para buscar o diretor de um filme
def get_diretor(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        credits = response.json()
        for crew_member in credits.get('crew', []):
            if crew_member['job'] == 'Director':
                return crew_member['name']
    return "Desconhecido"


def get_movies_by_most_voted() -> list[Movie]|None:
    movies = []
    count = 0
    for page in range(1,51): #20 filmes por pagina
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=vote_count.desc"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        }

        response = requests.get(url, headers=headers)
        print(f"PAGE {page}")
        if response.status_code == 200:
            filmes = response.json().get('results', [])
            for filme in filmes:
                movie_id = filme['id']
                titulo = filme['title']
                ano = int(filme['release_date'].split("-")[0]) if filme['release_date'] else None
                poster_url = POSTER_BASE_URL + filme['poster_path'] if filme['poster_path'] else None
                diretor = get_diretor(movie_id)
                count = count + 1
                print(f"{count} -> {movie_id, titulo, diretor, ano}")
                movies.append(Movie(movie_id, titulo, diretor, ano, poster_url, 1400))
            app_logger.info(f"{count} most voted movies fetched from TMDB")

        else:
            error_logger.error(f"Error when accessing page {page}: {response.status_code}")
            break

    return movies


def get_movies_by_top_rated() -> list[Movie]|None:
    movies = []
    count = 0
    for page in range(1,51): #20 filmes por pagina
        url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page}"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        }

        response = requests.get(url, headers=headers)

        print(f"PAGE {page}")
        if response.status_code == 200:
            filmes = response.json().get('results', [])
            for filme in filmes:
                movie_id = filme['id']
                titulo = filme['title']
                ano = int(filme['release_date'].split("-")[0]) if filme['release_date'] else None
                poster_url = POSTER_BASE_URL + filme['poster_path'] if filme['poster_path'] else None
                diretor = get_diretor(movie_id)
                count = count + 1
                print(f"{count} -> {movie_id, titulo, diretor, ano}")
                movies.append(Movie(movie_id, titulo, diretor, ano, poster_url, 1400))
            app_logger.info(f"{count} top rated movies fetched from TMDB")

        else:
            error_logger.error(f"Error when accessing page {page}: {response.status_code}")
            break

    return movies


def insert_movies(movie_set:set[Movie]):
    query = """
        INSERT INTO movies (id, title, director, year, poster_url, elo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    list_of_tuples = [(movie.id,movie.title,movie.director,movie.year,movie.poster_url,movie.elo) for movie in movie_set]
    try:
        conn = connect(**configure)
        with conn.cursor() as cur:
            cur.executemany(query, list_of_tuples)
            app_logger.info(f"{cur.rowcount} movies inserted successfully.")
        conn.commit()  # Salva as alterações no banco
    except Error as e:
        error_logger.error(f"Error inserting movies: {e}")
        conn.rollback()  # Reverte as alterações em caso de erro
    finally:
        if conn.is_connected():
            conn.close()


def insert_movies_from_list(movie_list:set[Movie]):
    insert_query = """
        INSERT INTO movies (id, title, director, year, poster_url, elo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    verification_query = "SELECT COUNT(*) FROM movies WHERE id = %s"
    count = 0
    try:
        conn = connect(**configure)
        with conn.cursor() as cur:
            for movie in movie_list:
                cur.execute(verification_query, (movie.id,))
                res = cur.fetchone()

                if res[0] == 0:
                    cur.execute(insert_query, (movie.id, movie.title, movie.director, movie.year, movie.poster_url, movie.elo))
                    conn.commit()
                    count += 1
                    #app_logger.info(f"Movie {movie.title} inserted successfully.")
                else:
                    print(f"Movie {movie.title} is already in the database.")
        conn.commit()
        app_logger.info(f"{count} movies inserted successfully")
    except Error as e:
        error_logger.error(f"Error inserting movies: {e}")
        conn.rollback()
    finally:
        if conn.is_connected(): conn.close()



def init_db():
    """
    Inicializa o banco de dados:
    - Cria o banco de dados, se necessário.
    - Cria as tabelas definidas no script SQL.
    """
    try:
        if create_database_if_not_exists():
            app_logger.info("Database creation step completed successfully.")
        else:
            app_logger.info("Database already exists or creation step was skipped.")

        create_tables_if_not_exists(create_tables_script)
        app_logger.info("Tables creation step completed successfully.")

        if is_table_empty("movies"):
            insert_movies(get_movies_by_most_voted())
            insert_movies_from_list(get_movies_by_top_rated())
            app_logger.info("Movies insertion step completed.")
        else:
            app_logger.info("Table 'movies' is not empty.")

    except Exception as e:
        error_logger.error(f"Error during database initialization: {e}")