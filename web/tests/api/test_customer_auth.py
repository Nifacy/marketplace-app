from tests import utils
from app import schemas
import pytest


@pytest.mark.asyncio
async def test_invalid_data(test_client):
    response = test_client.post("/customer/register", json={"info": "invalid"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_successful_registration(test_client):
    supplier_info = utils.create_customer_info_sample()
    customer_credentials = schemas.CustomerCredentials(
        login="test-supplier",
        password="Password12345&!",
    )
    register_form = schemas.CustomerRegisterForm(
        credentials=customer_credentials,
        info=supplier_info,
    )

    response = test_client.post("/customer/register", json=register_form.model_dump())
    assert response.status_code == 200
    assert "token" in response.json()


@pytest.mark.asyncio
async def test_nonexistent_user(test_client):
    credentials = schemas.CustomerCredentials(
        login="test-supplier",
        password="Password12345&!",
    )
    response = test_client.post("/customer/login", json=credentials.model_dump())
    assert response.status_code == 401

@pytest.mark.asyncio
def test_wrong_password(test_client):
    supplier_info = utils.create_customer_info_sample()
    customer_credentials = schemas.CustomerCredentials(
        login="test-supplier",
        password="Password12345&!",
    )
    register_form = schemas.CustomerRegisterForm(
        credentials=customer_credentials,
        info=supplier_info,
    )

    test_client.post("/customer/register", json=register_form.model_dump())
    
    customer_credentials.password = f"wrong-{customer_credentials.password}"
    response = test_client.post("/customer/login", json=customer_credentials.model_dump())
    assert response.status_code == 401

@pytest.mark.asyncio
def test_successful_login(test_client):
    supplier_info = utils.create_customer_info_sample()
    customer_credentials = schemas.CustomerCredentials(
        login="test-supplier",
        password="Password12345&!",
    )
    register_form = schemas.CustomerRegisterForm(
        credentials=customer_credentials,
        info=supplier_info,
    )

    test_client.post("/customer/register", json=register_form.model_dump())
    response = test_client.post("/customer/login", json=customer_credentials.model_dump())

    assert response.status_code == 200
    assert "token" in response.json()
