import pytest

from app import schemas
from tests import utils


@pytest.mark.asyncio
async def test_get_current_supplier(test_client):
    register_form = utils.create_supplier_register_form()
    response = test_client.post("/supplier/register", json=register_form.model_dump())
    assert response.status_code == 200
    token = schemas.Token.model_validate(response.json())

    headers = {"Authorization": f"Bearer {token.token}"}
    response = test_client.get("/supplier/me", headers=headers)

    assert response.status_code == 200
    customer = schemas.Supplier.model_validate(response.json())
    assert customer.info == register_form.info
