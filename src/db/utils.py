import os
import psycopg
from dotenv import load_dotenv


def get_db_credentials():
    load_dotenv()
    return {
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "host": os.environ["DB_HOST"],
        "port": os.environ["DB_PORT"],
        "dbname": os.environ["DB_NAME"],
    }


def get_connection_string():
    credentials = get_db_credentials()
    user = credentials["user"]
    password = credentials["password"]
    host = credentials["host"]
    port = credentials["port"]
    dbname = credentials["dbname"]

    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"


def connect_to_db():
    credentials = get_db_credentials()
    connection = psycopg.connect(**credentials)
    cursor = connection.cursor(row_factory=psycopg.rows.dict_row)
    return connection, cursor
