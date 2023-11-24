import pytest

from app.schemas import SupplierInfo, Address, Contacts
from app.usecases import supplier


_counter = 0


def create_supplier_sample() -> SupplierInfo:
    global _counter
    _counter += 1

    return SupplierInfo(
        name=f'test-supplier-{_counter}',
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


def test_supplier_creation(db_connection):
    expected_supplier = create_supplier_sample()
    supplier_id = supplier.create_supplier(db_connection, expected_supplier)
    _supplier = supplier.get_supplier(db_connection, supplier_id)

    assert _supplier.info == expected_supplier


def test_supplier_not_found(db_connection):
    with pytest.raises(supplier.SupplierNotFound):
        supplier.get_supplier(db_connection, 1)

    db_connection.close()
