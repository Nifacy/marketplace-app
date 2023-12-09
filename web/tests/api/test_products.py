from fastapi.testclient import TestClient
from app import schemas
from app.dependencies import database
from app.usecases import product, supplier, customer, oauth2, favorites

from tests import utils


# TODO: change after creation endpoint realization
def create_product(info: schemas.ProductInfo, supplier: schemas.Supplier) -> schemas.Product:
    return product.create_product(
        database.get_connection(),
        supplier,
        info,
    )

def _get_token(test_client: TestClient, credentials: schemas.CustomerCredentials | schemas.SupplierCredentials) -> schemas.Token:
    if isinstance(credentials, schemas.CustomerCredentials):
        login_endpoint = "/customer/login"
    else:
        login_endpoint = "/supplier/login"

    print(f'[info] {credentials.model_dump()}')

    response = test_client.post(
        login_endpoint,
        json=credentials.model_dump(),
    )

    return schemas.Token.model_validate(response.json())

# TODO: change return type after bound endpoints realization
def create_supplier(test_client: TestClient) -> tuple[schemas.Token, schemas.Supplier]:
    register_form = utils.create_supplier_register_form()
    _supplier = supplier.register_supplier(
        database.get_connection(),
        register_form,
    )
    token = _get_token(test_client, register_form.credentials)
    return token, _supplier

# TODO: change return type after bound endpoints realization
def create_customer(test_client: TestClient) -> tuple[schemas.Token, schemas.Customer]:
    register_form = utils.create_customer_register_form()
    _customer = customer.register_customer(
        database.get_connection(),
        register_form,
    )
    token = _get_token(test_client, register_form.credentials)
    return token, _customer

def create_products_sample(test_client: TestClient) -> list[schemas.Product]:
    _, supplier_a = create_supplier(test_client)
    _, supplier_b = create_supplier(test_client)
    conn = database.get_connection()

    products_info = [
        (supplier_a, utils.create_product_info_sample(product_name='a-1')),
        (supplier_a, utils.create_product_info_sample(product_name='a-2')),
        (supplier_b, utils.create_product_info_sample(product_name='b-1')),
        (supplier_b, utils.create_product_info_sample(product_name='b-2')),
        (supplier_b, utils.create_product_info_sample(product_name='b-3')),
    ]

    return [
        product.create_product(conn, _supplier, product_info)
        for _supplier, product_info in products_info
    ]

# TODO: change after creation endpoint realization
def add_to_favorites(test_client: TestClient, token: schemas.Token, product_id: int) -> None:
    customer_id = oauth2.decode_token(token.token).id
    favorites.add_to_favorite(
        database.get_connection(),
        customer_id,
        product_id,
    )

def get_products(test_client: TestClient, token: schemas.Token, name: str | None = None) -> list[schemas.Product]:
    params = {"name": name} if name is not None else {}
    headers = {"Authorization": f"Bearer {token.token}"}
    response = test_client.get("/product", params=params, headers=headers)

    assert response.status_code == 200
    return [schemas.Product.model_validate(p) for p in response.json()]

# tests

def test_blocks_not_authenticated_requests(test_client):
    response = test_client.get("/product")
    assert response.status_code == 401

def test_get_all_products(test_client):
    supplier_token, _ = create_supplier(test_client)
    products = create_products_sample(test_client)
    assert get_products(test_client, supplier_token) == products

def test_get_products_by_name_filter(test_client):
    supplier_token, _ = create_supplier(test_client)
    products = create_products_sample(test_client)
    assert get_products(test_client, supplier_token, 'a') == products[:2]
    assert get_products(test_client, supplier_token, 'b') == products[2:]
    assert get_products(test_client, supplier_token, 'c') == []

def test_favorites_available_for_customer(test_client):
    customer_token, _ = create_customer(test_client)
    products = create_products_sample(test_client)
    favorite_products = products[::2]

    for favorite_product in favorite_products:
        add_to_favorites(test_client, customer_token, favorite_product.id)

    found_products = get_products(test_client, customer_token)

    for p in found_products:
        if p in favorite_products:
            assert p.in_favorites
