import psycopg2
from app.config import settings


def _init_db(conn):
    cur = conn.cursor()

    files = ['sql/initialise.sql', 'sql/address.sql', 'sql/contacts.sql', 'sql/supplier.sql']

    for file in files:
        with open(file, 'r') as f:
            cur.execute(f.read())

    cur.close()


def connect():
    conn = psycopg2.connect(str(settings.database_url))
    _init_db(conn)
    return conn
