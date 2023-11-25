import pytest

from app.usecases import supplier, product

from . import utils


def test_product_creation(db_connection):
    _supplier = supplier.create_supplier(
        db_connection,
        utils.create_supplier_info_sample(),
    )
    product_info = utils.create_product_info_sample(_supplier)
    _product = product.create_product(db_connection, product_info)

    assert _product.info == product_info


def test_product_getable_after_creation(db_connection):
    _supplier = supplier.create_supplier(
        db_connection,
        utils.create_supplier_info_sample(),
    )
    product_info = utils.create_product_info_sample(_supplier)
    created_product = product.create_product(db_connection, product_info)
    found_product, = product.get_products(
        db_connection,
        product.SearchFilters(created_product.id),
    )

    assert created_product == found_product


def test_products_not_found(db_connection):
    products = product.get_products(db_connection, product.SearchFilters(1))
    assert len(products) == 0
