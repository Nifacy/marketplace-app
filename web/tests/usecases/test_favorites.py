import pytest

from app import schemas
from app.usecases import customer, favorites, product, supplier
from tests import utils


def _create_customer(conn) -> schemas.Customer:
    return customer.create_customer(
        conn,
        utils.create_customer_info_sample(),
    )


def _create_product(conn) -> schemas.Product:
    supplier_info = utils.create_supplier_info_sample()
    _supplier = supplier.create_supplier(conn, supplier_info)

    product_info = utils.create_product_info_sample()
    _product = product.create_product(conn, _supplier, product_info)

    return _product


def test_cant_add_non_existent_customer(db_connection):
    _product = _create_product(db_connection)

    with pytest.raises(favorites.CustomerNotFound):
        favorites.add_to_favorite(db_connection, -1, _product.id)


def test_cant_add_non_existent_product(db_connection):
    _customer = _create_customer(db_connection)

    with pytest.raises(favorites.ProductNotFound):
        favorites.add_to_favorite(db_connection, _customer.id, -1)


def test_getable_after_added_to_favorites(db_connection):
    _product = _create_product(db_connection)
    _customer = _create_customer(db_connection)

    favorites.add_to_favorite(db_connection, _customer.id, _product.id)
    favorite_products = favorites.get_favorites(db_connection, _customer.id)

    assert favorite_products == [_product]


def test_cant_remove_non_existent_customer(db_connection):
    _product = _create_product(db_connection)

    with pytest.raises(favorites.CustomerNotFound):
        favorites.remove_from_favorites(db_connection, -1, _product.id)


def test_cant_remove_non_existent_product(db_connection):
    _customer = _create_customer(db_connection)

    with pytest.raises(favorites.ProductNotFound):
        favorites.remove_from_favorites(db_connection, _customer.id, -1)


def test_cant_get_after_remove(db_connection):
    _product = _create_product(db_connection)
    _customer = _create_customer(db_connection)

    favorites.add_to_favorite(db_connection, _customer.id, _product.id)
    favorites.remove_from_favorites(db_connection, _customer.id, _product.id)

    assert favorites.get_favorites(db_connection, _customer.id) == []


def test_emty_set_of_favorites(db_connection):
    _customer = _create_customer(db_connection)
    assert favorites.get_favorites(db_connection, _customer.id) == []
