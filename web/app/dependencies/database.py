import psycopg2.extensions
from app import database


_connection: psycopg2.extensions.connection | None = None


def open_connection() -> None:
    global _connection
    assert _connection is None

    _connection = database.connect(database.from_settings)


def get_connection() -> psycopg2.extensions.connection:
    assert _connection is not None
    return _connection


def close_connection():
    global _connection
    assert _connection is not None
    
    _connection.close()
    _connection = None
