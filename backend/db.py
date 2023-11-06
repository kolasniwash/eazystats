import os
from dotenv import load_dotenv
from contextlib import contextmanager
import psycopg2

load_dotenv()


def get_postgres_connection_details():
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv("HOST_PORT")
    password = os.environ.get("POSTGRES_PASSWORD", "abc123")
    schema = os.getenv("POSTGRES_SCHEMA")
    user = os.getenv("POSTGRES_USER")
    database = os.getenv("POSTGRES_DB")
    return database, user, password, host, port, schema

@contextmanager
def get_postgres_connection():
    database, user, password, host, port, schema = get_postgres_connection_details()

    connection = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    try:
        yield connection
    finally:
        connection.close()