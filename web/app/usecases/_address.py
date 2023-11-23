from ast import Add
from audioop import add
import psycopg2.extras
import psycopg2
from app.schemas import Address
from ._exceptions import AddressNotFound


def get_address(conn: psycopg2.extensions.connection, address_id: int) -> Address:
    cur = conn.cursor()

    cur.callproc('get_address', (address_id,))

    address_data = cur.fetchone()

    if address_data is None:
        raise AddressNotFound()

    address = Address(
            street=address_data[1],
            city=address_data[2],
            country=address_data[3],
            postal_code=address_data[4],
            house=address_data[5],
            entrance=address_data[6],
            appartment=address_data[7],
        )

    cur.close()

    return address


def create_address(conn: psycopg2.extensions.connection, address: Address) -> int:
    cur = conn.cursor()

    cur.callproc(
        'create_address', 
        (
            address.street, 
            address.city, 
            address.country, 
            address.postal_code, 
            address.house, 
            address.entrance, 
            address.appartment
            )
        )

    address_id = cur.fetchone()[0]

    cur.close()

    return address_id