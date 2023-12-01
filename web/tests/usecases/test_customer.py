import pytest

from app.schemas import CustomerCredentials, CustomerRegisterForm
from app.usecases import customer

from . import utils


def test_customer_creation(db_connection):
    expected_customer_info = utils.create_customer_info_sample()
    created_customer = customer.create_customer(db_connection, expected_customer_info)
    
    assert created_customer.info == expected_customer_info


def test_customer_getable_after_creation(db_connection):
    expected_customer_info = utils.create_customer_info_sample()
    created_customer = customer.create_customer(db_connection, expected_customer_info)
    found_customer = customer.get_customer(db_connection, created_customer.id)

    assert created_customer == found_customer


def test_customer_not_found(db_connection):
    with pytest.raises(customer.CustomerNotFound):
        customer.get_customer(db_connection, 1)


def test_customer_exists_after_registration(db_connection):
    customer_form = CustomerRegisterForm(
        credentials=CustomerCredentials(
            login="customer",
            password="Test@1234",
        ),
        info=utils.create_customer_info_sample(),
    )

    created_customer = customer.register_customer(db_connection, customer_form)
    found_customer = customer.get_customer(db_connection, created_customer.id)

    assert created_customer == found_customer


def test_can_login_after_success_registration(db_connection):
    customer_credentials = CustomerCredentials(
        login="customer",
        password="Test@1234",
    )

    customer_form = CustomerRegisterForm(
        credentials=customer_credentials,
        info=utils.create_customer_info_sample(),
    )

    created_customer = customer.register_customer(db_connection, customer_form)
    authorised_customer = customer.login_customer(db_connection, customer_credentials)

    assert created_customer == authorised_customer


def test_cant_register_already_exists_customer(db_connection):
    customer_credentials = CustomerCredentials(
        login="customer",
        password="Test@1234",
    )

    customer_form = CustomerRegisterForm(
        credentials=customer_credentials,
        info=utils.create_customer_info_sample(),
    )

    customer.register_customer(db_connection, customer_form)

    with pytest.raises(customer.CustomerAlreadyExists):
        customer.register_customer(db_connection, customer_form)


def test_cant_login_if_customer_not_exists(db_connection):
    customer_credentials = CustomerCredentials(
        login="not-exists-customer",
        password="Test@1234",
    )

    with pytest.raises(customer.InvalidCredentials):
        customer.login_customer(db_connection, customer_credentials)
