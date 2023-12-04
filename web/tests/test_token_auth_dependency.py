import contextlib
from typing import Iterator

import pytest
from fastapi import HTTPException
from jose import jwt

from app import schemas
from app.dependencies import AccountAuthenticator
from app.usecases import customer, oauth2, supplier
from tests import utils


@contextlib.contextmanager
def raises_unautharized_error() -> Iterator[None]:
    with pytest.raises(HTTPException) as exc:
        yield

    assert exc.value.status_code == 401


def test_get_current_user_supplier(db_connection):
    supplier_info = utils.create_supplier_info_sample()
    created_supplier = supplier.create_supplier(db_connection, supplier_info)
    token_data = schemas.TokenData(type="supplier", id=created_supplier.id)
    token = oauth2.generate_token(token_data)

    authenticiator = AccountAuthenticator(db_connection)
    user = authenticiator(token)

    assert isinstance(user, schemas.Supplier)
    assert user == created_supplier


def test_get_current_user_customer(db_connection):
    customer_info = utils.create_customer_info_sample()
    created_customer = customer.create_customer(db_connection, customer_info)
    token_data = schemas.TokenData(type="customer", id=created_customer.id)
    token = oauth2.generate_token(token_data)

    authenticiator = AccountAuthenticator(db_connection)
    user = authenticiator(token)

    assert isinstance(user, schemas.Customer)
    assert user == created_customer


def test_get_non_existent_user(db_connection):
    authenticiator = AccountAuthenticator(db_connection)
    non_existent_supplier = schemas.TokenData(type="supplier", id=-1)
    non_existent_customer = schemas.TokenData(type="customer", id=-1)

    with raises_unautharized_error():
        token = oauth2.generate_token(non_existent_supplier)
        authenticiator(token)

    with raises_unautharized_error():
        token = oauth2.generate_token(non_existent_customer)
        authenticiator(token)


@pytest.mark.parametrize(
    "sample",
    [
        {"type": "unknown-type", "id": 100},
        {"type": "supplier", "id": "wrong-type-id"},
        {"foo": "bar"},
    ],
)
def test_validation_token_handles(db_connection, sample):
    token = jwt.encode(sample, "VERY_SECRET_KEY", algorithm="HS256")
    authenticiator = AccountAuthenticator(db_connection)

    with raises_unautharized_error():
        authenticiator(token)


def test_get_current_user_random_string(db_connection):
    token = "random_string"
    authenticiator = AccountAuthenticator(db_connection)

    with raises_unautharized_error():
        authenticiator(token)
