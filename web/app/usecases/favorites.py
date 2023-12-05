from enum import Enum
import psycopg2.extensions
from ._exceptions import UnableToAddToFavorite, ProductNotFound, CustomerNotFound
from . import product
from app.schemas import Product


class _StatusCode(Enum):
    OK = 0
    CUSTOMER_NOT_EXISTS = 1
    PRODUCT_NOT_EXISTS = 2


def _handle_status_code(status_code: _StatusCode) -> None:
    if status_code == _StatusCode.CUSTOMER_NOT_EXISTS:
        raise CustomerNotFound()

    if status_code == _StatusCode.PRODUCT_NOT_EXISTS:
        raise ProductNotFound()



def add_to_favorite(conn: psycopg2.extensions.connection, customer_id: int, product_id: int) -> None:
    cur = conn.cursor()
    cur.callproc('add_to_favorite', (customer_id, product_id))
    response = cur.fetchone()
    cur.close()

    if response is None:
        raise UnableToAddToFavorite()
    
    _handle_status_code(_StatusCode(response[0]))


def get_favorites(conn: psycopg2.extensions.connection, customer_id: int) -> list[Product]:
    cur = conn.cursor()
    cur.callproc('get_favorites', (customer_id,))
    found_records = cur.fetchall()
    cur.close()

    return list(product.deserialize_builds(conn, found_records))


def remove_from_favorites(conn: psycopg2.extensions.connection, customer_id: int, product_id: int) -> None:
    cur = conn.cursor()
    cur.callproc('remove_from_favorites', (customer_id, product_id))
    response = cur.fetchone()
    cur.close()

    if response is None:
        raise UnableToAddToFavorite()

    _handle_status_code(_StatusCode(response[0]))
