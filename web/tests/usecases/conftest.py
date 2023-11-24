import pytest
from app import database


@pytest.fixture
def db_connection():
    conn = database.connect(database.temporary_connection)
    yield conn
    conn.close()
