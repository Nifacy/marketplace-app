import pytest

from app.usecases import favorites, product, supplier, customer
from app import schemas
from tests import utils


def test_cant_add_non_existent_customer(db_connection):
    supplier_info = utils.create_supplier_info_sample()
    _supplier = supplier.create_supplier(db_connection, supplier_info)

    product_info = utils.create_product_info_sample()
    _product = product.create_product(db_connection, _supplier, product_info)

    with pytest.raises(favorites.CustomerNotFound):
        favorites.add_to_favorite(db_connection, -1, _product.id)


def test_cant_add_non_existent_product(db_connection):
    customer_info = utils.create_customer_info_sample()
    _customer = customer.create_customer(db_connection, customer_info)

    with pytest.raises(favorites.ProductNotFound):
        favorites.add_to_favorite(db_connection, _customer.id, -1)
