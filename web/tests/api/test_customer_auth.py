import pytest

from tests import utils


@pytest.mark.asyncio
async def test_invalid_data(test_client):
    response = test_client.post("/customer/register", json={"info": "invalid"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_successful_registration(test_client):
    register_form = utils.create_customer_register_form()
    response = test_client.post("/customer/register", json=register_form.model_dump())
    assert response.status_code == 200
    assert "token" in response.json()


@pytest.mark.asyncio
async def test_nonexistent_user(test_client):
    credentials = utils.create_customer_register_form().credentials
    response = test_client.post("/customer/login", json=credentials.model_dump())
    assert response.status_code == 401


@pytest.mark.asyncio
def test_wrong_password(test_client):
    register_form = utils.create_customer_register_form()

    test_client.post("/customer/register", json=register_form.model_dump())

    credentials = register_form.credentials
    credentials.password = f"wrong-{credentials.password}"

    response = test_client.post("/customer/login", json=credentials.model_dump())
    assert response.status_code == 401


@pytest.mark.asyncio
def test_successful_login(test_client):
    register_form = utils.create_customer_register_form()
    credentials = register_form.credentials

    test_client.post("/customer/register", json=register_form.model_dump())
    response = test_client.post("/customer/login", json=credentials.model_dump())

    assert response.status_code == 200
    assert "token" in response.json()
