from venv import create
import pytest
from app import schemas
from tests import utils
from app.usecases import customer

@pytest.mark.asyncio
async def test_get_customer_success(test_client, db_connection):
    expected_customer_info = utils.create_customer_info_sample()
    created_customer = customer.create_customer(db_connection, expected_customer_info)

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

