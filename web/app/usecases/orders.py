import psycopg2

from app.schemas import Customer, Order, OrderCreateSchema, OrderStatus
from ._exceptions import *
from ._address import get_address, create_address
from .customer import get_customer
from .product import _get_product


def _get_order(conn: psycopg2.extensions.connection, order_id: int) -> Order:
    cur = conn.cursor()

    cur.callproc('get_order', (order_id,))

    order_data = cur.fetchone()
    
    cur.close()

    if order_data is None:
        raise UnableToGetOrder()
    else:
        status_code = order_data[0]

        if status_code != 0:
            if status_code == 1:
                raise OrderNotFound()
            else:
                raise UnableToGetOrder(f"Unknown error occurred with status code {status_code}")

        order = Order(
            id=order_data[1],
            status=order_data[2],
            cancel_description=order_data[3],
            price=order_data[4],
            product=_get_product(conn, order_data[5]),
            creation_datetime=order_data[6],
            target_address=get_address(conn, order_data[7]),
            customer=get_customer(conn, order_data[8]),
        )

    return order



def create_order(conn: psycopg2.extensions.connection, order: OrderCreateSchema, customer: Customer) -> Order:
    cur = conn.cursor()

    address_id = create_address(conn, order.target_address)

    cur.callproc(
        'create_order', 
        (
            order.product_id, 
            address_id,
            customer.id,
        )
    )

    result = cur.fetchone()

    cur.close()

    if result is None:
        raise UnableToCreateOrder()
    else:
        status_code, order_id = result

        if status_code != 0:
            if status_code == 1:
                raise UnableToCreateOrder("The product does not exist.")
            else:
                raise UnableToCreateOrder(f"Unknown error occurred with status code {status_code}")

    return _get_order(conn, order_id)



def get_orders(
        conn: psycopg2.extensions.connection, 
        order_id: int | None = None, 
        supplier_id: int | None = None, 
        customer_id: int | None = None
) -> list[Order]:
    cur = conn.cursor()

    cur.callproc('get_orders', (order_id, supplier_id, customer_id))

    orders_data = cur.fetchall()
    orders = []

    cur.close()
    
    for order_data in orders_data:
        order = Order(
            id=order_data[0],
            status=order_data[1],
            cancel_description=order_data[2],
            price=order_data[3],
            product=_get_product(conn, order_data[4]), # FIX
            creation_datetime=order_data[5],
            target_address=get_address(conn, order_data[6]),
            customer=get_customer(conn, order_data[7]),
        )
        orders.append(order)

    return orders



def update_order_status(conn: psycopg2.extensions.connection, order_id: int, status: OrderStatus) -> Order:
    cur = conn.cursor()

    cur.callproc('update_order_status', (order_id, status))

    result = cur.fetchone()

    cur.close()

    if result is None:
        raise UnableToUpdateOrder()
    else:
        status_code = result[0]

        if status_code != 0:
            if status_code == 1:
                raise UnableToUpdateOrder("The order does not exist.")
            elif status_code == 2:
                raise UnableToUpdateOrder("The update failed.")
            else:
                raise UnableToUpdateOrder(f"Unknown error occurred with status code {status_code}")

    return _get_order(conn, order_id)

