import pytest

from app.schemas import SupplierInfo, Address, Contacts, SupplierRegisterForm, SupplierCredentials
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


def test_supplier_exists_after_registration(db_connection):
    supplier_form = SupplierRegisterForm(
        credentials=SupplierCredentials(
            login="supplier",
            password="123",
        ),
        info=create_supplier_sample(),
    )

    created_supplier = supplier.register_supplier(db_connection, supplier_form)
    found_supplier = supplier.get_supplier(db_connection, created_supplier.id)

    assert created_supplier == found_supplier


def test_can_login_after_success_registration(db_connection):
    supplier_credentials = SupplierCredentials(
        login="supplier",
        password="123",
    )

    supplier_form = SupplierRegisterForm(
        credentials=supplier_credentials,
        info=create_supplier_sample(),
    )

    created_supplier = supplier.register_supplier(db_connection, supplier_form)
    authorised_supplier = supplier.login_supplier(db_connection, supplier_credentials)

    assert created_supplier == authorised_supplier


def test_cant_register_already_exists_supplier(db_connection):
    supplier_credentials = SupplierCredentials(
        login="supplier",
        password="123",
    )

    supplier_form = SupplierRegisterForm(
        credentials=supplier_credentials,
        info=create_supplier_sample(),
    )

    supplier.register_supplier(db_connection, supplier_form)

    with pytest.raises(supplier.SupplierAlreadyExists):
        supplier.register_supplier(db_connection, supplier_form)


def test_cant_login_if_supplier_not_exists(db_connection):
    supplier_credentials = SupplierCredentials(
        login="not-exists-supplier",
        password="123",
    )

    with pytest.raises(supplier.InvalidCredentials):
        supplier.login_supplier(db_connection, supplier_credentials)
