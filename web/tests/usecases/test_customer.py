import pytest

from app.schemas import CustomerInfo, Address, Contacts
from app.usecases import customer


_counter = 0


def create_customer_sample() -> CustomerInfo:
    global _counter
    _counter += 1

    return CustomerInfo(
        first_name=f'customer-{_counter}',
        last_name='last-name',
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


def test_customer_creation(db_connection):
    expected_customer_info = create_customer_sample()
    created_customer = customer.create_customer(db_connection, expected_customer_info)
    
    assert created_customer.info == expected_customer_info


def test_customer_getable_after_creation(db_connection):
    expected_customer_info = create_customer_sample()
    created_customer = customer.create_customer(db_connection, expected_customer_info)
    found_customer = customer.get_customer(db_connection, created_customer.id)

    assert created_customer == found_customer


def test_customer_not_found(db_connection):
    with pytest.raises(customer.CustomerNotFound):
        customer.get_customer(db_connection, 1)
