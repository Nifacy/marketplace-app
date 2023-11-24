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
    expected_supplier_info = create_supplier_sample()
    created_supplier = supplier.create_supplier(db_connection, expected_supplier_info)

    assert created_supplier.info == expected_supplier_info


def test_supplier_getable_after_creation(db_connection):
    expected_supplier_info = create_supplier_sample()
    created_supplier = supplier.create_supplier(db_connection, expected_supplier_info)
    found_supplier = supplier.get_supplier(db_connection, created_supplier.id)

    assert created_supplier == found_supplier


def test_supplier_not_found(db_connection):
    with pytest.raises(supplier.SupplierNotFound):
        supplier.get_supplier(db_connection, 1)

    db_connection.close()
