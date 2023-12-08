import psycopg2

from app.schemas import Customer, Order, OrderCreateSchema, OrderStatus
from ._exceptions import *
from ._address import get_address, create_address


def _get_order(conn: psycopg2.extensions.connection, order_id: int) -> Order:
    cur = conn.cursor()

    cur.callproc('get_order', (order_id,))

    order_data = cur.fetchone()
    # Никогда не произойдет, брух. Юзается только тогда, когда создаем. Зачем тут вообще исключение.
    if order_data is None:
        raise OrderNotFound() 

    order = Order(
        id=order_data[0],
        status=order_data[1],
        cancel_description=order_data[2],
        price=order_data[3],
        product_id=order_data[4],
        creation_datetime=order_data[5],
        target_address=get_address(conn, order_data[6]),
        customer_id=order_data[7],
    )

    cur.close()

    return order


def create_order(conn: psycopg2.extensions.connection, order: OrderCreateSchema, customer: Customer) -> Order:
    cur = conn.cursor()

    address_id = create_address(conn, order.target_address)

    try:
        cur.callproc(
            'create_order', 
            (
                order.product_id, 
                address_id,
                customer.id,
            )
        )
    except psycopg2.errors.RaiseException as e:
        if 'Product does not exist' in str(e):
            raise UnableToCreateOrder("The product does not exist.")
        else:
            raise e

    result = cur.fetchone()

    if result is None:
        raise UnableToCreateOrder()
    else:
        order_id = result[0]

    cur.close()

    return _get_order(conn, order_id)


def get_orders(conn: psycopg2.extensions.connection, order_id: int | None = None, supplier_id: int | None = None, customer_id: int | None = None) -> list[Order]:
    cur = conn.cursor()

    cur.callproc('get_orders', (order_id, supplier_id, customer_id))

    orders_data = cur.fetchall()
    orders = []

    for order_data in orders_data:
        order = Order(
            id=order_data[0],
            status=order_data[1],
            cancel_description=order_data[2],
            price=order_data[3],
            product_id=order_data[4],
            creation_datetime=order_data[5],
            target_address=get_address(conn, order_data[6]),
            customer_id=order_data[7],
        )
        orders.append(order)

    cur.close()

    return orders



def update_order_status(conn: psycopg2.extensions.connection, order_id: int, status: OrderStatus) -> Order:
    cur = conn.cursor()

    cur.callproc('update_order_status', (order_id, status))

    cur.close()

    return _get_order(conn, order_id)
