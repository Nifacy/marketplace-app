from venv import create
import pytest
from app import schemas
from tests import utils
from app.usecases import customer
from app.dependencies.database import get_connection

# TODO: fix after db_connection is fixed
@pytest.mark.asyncio
async def test_get_customer_success(test_client):
    expected_customer_info = utils.create_customer_info_sample()
    created_customer = customer.create_customer(get_connection(), expected_customer_info)

    response = test_client.get(f"/customer/{created_customer.id}")

    assert response.status_code == 200
    assert response.json() == created_customer.model_dump()

@pytest.mark.asyncio
async def test_get_customer_not_found(test_client):
    non_existent_id = -1

    response = test_client.get(f"/customer/{non_existent_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}  

@pytest.mark.asyncio
async def test_get_customer_invalid_data_format(test_client):
    invalid_id = "invalid"

    response = test_client.get(f"/customer/{invalid_id}")

    assert response.status_code == 422
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_get_current_customer(test_client):
    register_form = utils.create_customer_register_form()
    response = test_client.post("/customer/register", json=register_form.model_dump())
    assert response.status_code == 200
    token = schemas.Token.model_validate(response.json())

    headers = {"Authorization": f"Bearer {token.token}"}
    response = test_client.get("/customer/me", headers=headers)

    print(response.json())
    assert response.status_code == 200
    customer = schemas.Customer.model_validate(response.json())
    assert customer.info == register_form.info
