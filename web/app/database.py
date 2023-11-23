import psycopg2
from psycopg2.extensions import connection

from .config import settings


def _init_db(conn: connection) -> None:
    cur = conn.cursor()
    with open('sql/initialise.sql', 'r') as f:
        cur.execute(f.read())
    conn.commit()


def connect() -> connection:
    conn = psycopg2.connect(str(settings.database_url))
    _init_db(conn)
    return conn
