from fastapi import status, HTTPException
from pydantic import ValidationError
import pytest

from app.schemas import TokenData, Supplier, Customer
from app.usecases.oauth2 import generate_token, verify_access_token, get_current_user
from app.usecases import customer, supplier

from . import utils


def test_token_encoding_and_decoding():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    data = TokenData(type='supplier', id=123)

    token = generate_token(data)
    decoded_data = verify_access_token(token, credentials_exception)

    assert decoded_data == data


def test_get_current_user_supplier(db_connection):
    supplier_info = utils.create_supplier_info_sample()
    created_supplier = supplier.create_supplier(db_connection, supplier_info)
    token_data = TokenData(type='supplier', id=created_supplier.id)
    token = generate_token(token_data)

    user = get_current_user(db_connection, token)

    assert isinstance(user, Supplier)
    assert user.id == created_supplier.id
    # TODO: Add more assertions to check the other attributes of the user if needed (don't think so)
    # idk, in case of data corruption???


def test_get_current_user_customer(db_connection):
    customer_info = utils.create_customer_info_sample()
    created_customer = customer.create_customer(db_connection, customer_info)
    token_data = TokenData(type='customer', id=created_customer.id)
    token = generate_token(token_data)

    user = get_current_user(db_connection, token)

    assert isinstance(user, Customer)
    assert user.id == created_customer.id
    # TODO: Add more assertions to check the other attributes of the user if needed (don't think so)
    # idk, in case of data corruption???


def test_get_current_user_invalid_token_data(db_connection):
    token_data_dict = {"type": "invalid_type", "id": 99999}
    with pytest.raises(ValidationError):
        token_data = TokenData(**token_data_dict)
        _ = generate_token(token_data)


def test_get_current_user_random_string(db_connection):
    token = "random_string"

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(db_connection, token)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_non_existent_user(db_connection):
    token_data = TokenData(type='supplier', id=99999)
    token = generate_token(token_data)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(db_connection, token)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED