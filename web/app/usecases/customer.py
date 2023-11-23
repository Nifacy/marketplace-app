import psycopg2.extras
import psycopg2
from app.schemas import Customer, CustomerInfo
from ._exceptions import *
from ._address import get_address, create_address
from ._contact import get_contact, create_contact


def get_customer(conn: psycopg2.extensions.connection, customer_id: int) -> Customer:
    cur = conn.cursor()

    cur.callproc('get_customer', (customer_id,))

    # 0 - id; 1 - first_name; 2 - last_name; 3 - contact; 4 - address
    customer_data = cur.fetchone()

    contacts = get_contact(conn, customer_data[3])
    address = get_address(conn, customer_data[4])

    if customer_data is None:
        raise CustomerNotFound()
    
    customer_info = CustomerInfo(
        first_name=customer_data[1],
        last_name=customer_data[2],
        contacts=contacts,
        address=address
    )
    customer = Customer(
        id=customer_data[0],
        info=customer_info
    )

    conn.commit()
    cur.close()

    return customer


def create_customer(conn: psycopg2.extensions.connection, customer: Customer) -> None:
    cur = conn.cursor()

    address_id = create_address(conn, customer.info.address)
    contact_id = create_contact(conn, customer.info.contacts)

    cur.callproc('create_customer', (customer.id, customer.info.first_name, customer.info.last_name, contact_id, address_id))

    conn.commit()
    cur.close()
