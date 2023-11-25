import pytest

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
