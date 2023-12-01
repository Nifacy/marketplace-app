import pytest
from app.schemas import SupplierRegisterForm, SupplierCredentials
from app.usecases import supplier
from . import utils


def test_supplier_creation(db_connection):
    supplier_info_sample = utils.create_supplier_info_sample()
    created_supplier = supplier.create_supplier(db_connection, supplier_info_sample)

    assert created_supplier.info == supplier_info_sample


def test_supplier_getable_after_creation(db_connection):
    supplier_info_sample = utils.create_supplier_info_sample()
    created_supplier = supplier.create_supplier(db_connection, supplier_info_sample)
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
            password="Test@1234",
        ),
        info=utils.create_supplier_info_sample(),
    )

    created_supplier = supplier.register_supplier(db_connection, supplier_form)
    found_supplier = supplier.get_supplier(db_connection, created_supplier.id)

    assert created_supplier == found_supplier


def test_can_login_after_success_registration(db_connection):
    supplier_credentials = SupplierCredentials(
        login="supplier",
        password="Test@1234",
    )

    supplier_form = SupplierRegisterForm(
        credentials=supplier_credentials,
        info=utils.create_supplier_info_sample(),
    )

    created_supplier = supplier.register_supplier(db_connection, supplier_form)
    authorised_supplier = supplier.login_supplier(db_connection, supplier_credentials)

    assert created_supplier == authorised_supplier


def test_cant_register_already_exists_supplier(db_connection):
    supplier_credentials = SupplierCredentials(
        login="supplier",
        password="Test@1234",
    )

    supplier_form = SupplierRegisterForm(
        credentials=supplier_credentials,
        info=utils.create_supplier_info_sample(),
    )

    supplier.register_supplier(db_connection, supplier_form)

    with pytest.raises(supplier.SupplierAlreadyExists):
        supplier.register_supplier(db_connection, supplier_form)


def test_cant_login_if_supplier_not_exists(db_connection):
    supplier_credentials = SupplierCredentials(
        login="not-exists-supplier",
        password="Test@1234",
    )

    with pytest.raises(supplier.InvalidCredentials):
        supplier.login_supplier(db_connection, supplier_credentials)
