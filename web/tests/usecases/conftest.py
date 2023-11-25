import pytest
import itertools
from psycopg2.extensions import connection

from app import database
from app.schemas import Address, Contacts, SupplierInfo

@pytest.fixture
def db_connection() -> connection:
    conn = database.connect(database.temporary_connection)
    yield conn
    conn.close()

_counter = itertools.count(start=1)

@pytest.fixture
def supplier_info_sample() -> SupplierInfo:
    count = next(_counter)

    return SupplierInfo(
        name=f'test-supplier-{count}',
        contacts=Contacts(
            phone='+1 (123) 456-7890',
            email='test.email@mail.com',
            telegram='@testsupplier',
        ),
        address=Address(
            street='Street',
            city='Moscow',
            country='Russia',
            postal_code='12345',
            house=1,
            entrance=1,
            appartment=1,
        )
    )
