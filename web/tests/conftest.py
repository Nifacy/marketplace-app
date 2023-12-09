import pytest
from psycopg2.extensions import connection

from app import database


@pytest.fixture
def db_connection() -> connection:
    conn = database.connect(database.temporary_connection)
    yield conn
    conn.close()
