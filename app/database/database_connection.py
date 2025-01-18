from app import config
from mysql.connector import connect, Error
from app.utils.logging_config import app_logger, error_logger

configure = {
    "user": f"{config.DB_USER}", 
    "password": f"{config.DB_PASSWORD}", 
    "host": f"{config.DB_HOST}", 
    "database": f"{config.DB_NAME}",
    "port": f"{config.DB_PORT}"
    }


def get_connection():
    try:
        connection = connect(**configure)
        if connection.is_connected():
            app_logger.info(f"Connection to database {configure['database']} was successfull.")
            return connection
    except Error as e:
        error_logger.error(f"Failed to establish connection to database {configure['database']}: {e}")
        return None

