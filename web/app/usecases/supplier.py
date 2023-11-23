import psycopg2.extras
import psycopg2
from app.schemas import Supplier
from ._exceptions import *
from ._address import get_address, create_address
from ._contact import get_contact, create_contact


def get_supplier(conn: psycopg2.extensions.connection, supplier_id: int) -> Supplier:
    cur = conn.cursor()

    cur.callproc('get_supplier', (supplier_id,))

    # 0 - id; 1 - name; 2 - contact; 3 - address
    supplier_data = cur.fetchone()

    contacts = get_contact(conn, supplier_data[2])
    address = get_address(conn, supplier_data[3])

    if supplier_data is None:
        raise SupplierNotFound()
    
    supplier = Supplier(
        id=supplier_data[0],
        name=supplier_data[1],
        contacts=contacts,
        address=address,
    )

    conn.commit()
    cur.close()
    
    return supplier


def create_supplier(conn: psycopg2.extensions.connection, supplier: Supplier) -> None:
    cur = conn.cursor()

    address_id = create_address(conn, supplier.address)
    contact_id = create_contact(conn, supplier.contacts)

    cur.callproc('create_supplier', (supplier.id, supplier.name, contact_id, address_id))

    conn.commit()
    cur.close()
