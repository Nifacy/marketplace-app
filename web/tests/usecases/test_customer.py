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
    expected_customer = create_customer_sample()
    customer_id = customer.create_customer(db_connection, expected_customer)
    _customer = customer.get_customer(db_connection, customer_id)

    assert _customer.info == expected_customer


def test_customer_not_found(db_connection):
    with pytest.raises(customer.CustomerNotFound):
        customer.get_customer(db_connection, 1)
