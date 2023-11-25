from typing import Callable
import psycopg2
from psycopg2.extensions import connection
from . import config


def _init_db(conn: connection) -> None:
    cur = conn.cursor()

    files = [
        'sql/initialise.sql',
        'sql/address.sql',
        'sql/contacts.sql',
        'sql/supplier.sql',
        'sql/customer.sql',
        'sql/product.sql',
    ]

    for file in files:
        with open(file, 'r') as f:
            cur.execute(f.read())

    cur.close()

def connect(create_connection: Callable[[str], connection]) -> connection:
    conn = create_connection(str(config.settings.database_url))
    _init_db(conn)
    return conn

# connection factories

def default_connection(url: str) -> connection:
    conn = psycopg2.connect(url)
    conn.autocommit = True
    return conn

def temporary_connection(url: str) -> connection:
    conn = psycopg2.connect(url)
    conn.autocommit = False
    return conn

def from_settings(url: str) -> connection:
    if config.settings.db_connection_type == config.DatabaseConnectionType.DEFAULT:
        return default_connection(url)
    
    elif config.settings.db_connection_type == config.DatabaseConnectionType.TEMPORARY:
        return temporary_connection(url)
    
    raise ValueError(f'Unknown database connection type : {config.settings.db_connection_type}')
