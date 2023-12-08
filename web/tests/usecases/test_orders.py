import pytest
from tests import utils

from app.usecases import supplier, product, customer, orders
from app.usecases._exceptions import *
from app import schemas


def setup_test_data(db_connection):
    supplier_info_sample = utils.create_supplier_info_sample()
    created_supplier = supplier.create_supplier(db_connection, supplier_info_sample)

    product_info_sample = utils.create_product_info_sample()
    created_product = product.create_product(db_connection, created_supplier, product_info_sample)

    customer_info = utils.create_customer_info_sample()
    created_customer = customer.create_customer(db_connection, customer_info)

    return created_supplier, created_product, created_customer


def test_order_creation_product_not_exists(db_connection):
    _, _, created_customer = setup_test_data(db_connection)

    order_sample = schemas.OrderCreateSchema(
        product_id=9999,
        target_address=utils.create_address_sample()
    )
    
    with pytest.raises(UnableToCreateOrder):
        _ = orders.create_order(db_connection, order_sample, created_customer)


def test_order_creation_success(db_connection):
    _, created_product, created_customer = setup_test_data(db_connection)

    order_sample = schemas.OrderCreateSchema(
        product_id=created_product.id,
        target_address=utils.create_address_sample()
    )

    created_order = orders.create_order(db_connection, order_sample, created_customer)

    assert created_order.product_id == created_product.id
    assert created_order.target_address == order_sample.target_address
    assert created_order.customer_id == created_customer.id


def test_order_search_filter(db_connection):
    _, created_product, created_customer = setup_test_data(db_connection)

    order_sample = schemas.OrderCreateSchema(
        product_id=created_product.id,
        target_address=utils.create_address_sample()
    )

    created_order = orders.create_order(db_connection, order_sample, created_customer)
    found_orders = orders.get_orders(db_connection, customer_id=created_customer.id)

    assert len(found_orders) > 0
    assert any(order.id == created_order.id for order in found_orders)
    for order in found_orders:
        assert order.customer_id == created_customer.id
        assert order.product_id == created_product.id


def test_order_status_update(db_connection):
    _, created_product, created_customer = setup_test_data(db_connection)
    
    order_sample = schemas.OrderCreateSchema(
        product_id=created_product.id,
        target_address=utils.create_address_sample()
    )

    created_order = orders.create_order(db_connection, order_sample, created_customer)
    updated_order = orders.update_order_status(db_connection, created_order.id, schemas.OrderStatus.paid)

    assert updated_order.status == schemas.OrderStatus.paid
    assert updated_order.id == created_order.id
    assert updated_order.product_id == created_product.id
    assert updated_order.customer_id == created_customer.id
