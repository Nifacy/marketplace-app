import psycopg2
from .config import settings

def _init_db(conn):
    cur = conn.cursor()
    with open('sql/initialise.sql', 'r') as f:
        cur.execute(f.read())
    conn.commit()

def connect():
    conn = psycopg2.connect(
        dbname=settings.database_name,
        user=settings.database_username,
        password=settings.database_password,
        host=settings.database_hostname
    )
    _init_db(conn)
    return conn
