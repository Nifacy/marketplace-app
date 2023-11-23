import psycopg2.extras
import psycopg2
from app.schemas import Address
from ._exceptions import AddressNotFound


def get_address(conn: psycopg2.extensions.connection, address_id: int):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.callproc('get_address', (address_id,))

    address_data = cur.fetchone()

    if address_data is None:
        raise AddressNotFound()

    address = Address(
            house=address_data[0],
            street=address_data[1],
            city=address_data[2],
            country=address_data[3],
            postal_code=address_data[4],
            entrance=address_data[5],
            appartment=address_data[6]
        )
    
    conn.commit()
    cur.close()

    return address