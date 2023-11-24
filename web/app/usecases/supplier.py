import psycopg2.extras
import psycopg2
from app.schemas import Supplier, SupplierInfo
from ._exceptions import *
from ._address import get_address, create_address
from ._contacts import get_contacts, create_contacts


def get_supplier(conn: psycopg2.extensions.connection, supplier_id: int) -> Supplier:
    cur = conn.cursor()

    cur.callproc('get_supplier', (supplier_id,))

    # 0 - id; 1 - name; 2 - contacts; 3 - address
    supplier_data = cur.fetchone()

    if supplier_data is None:
        raise SupplierNotFound()

    contacts = get_contacts(conn, supplier_data[2])
    address = get_address(conn, supplier_data[3])
    
    supplier_info = SupplierInfo(
        name=supplier_data[1],
        contacts=contacts,
        address=address,
    )
    supplier = Supplier(
        id=supplier_data[0],
        info=supplier_info
    )

    cur.close()

    return supplier


def create_supplier(conn: psycopg2.extensions.connection, supplier_info: SupplierInfo) -> Supplier:
    cur = conn.cursor()

    address_id = create_address(conn, supplier_info.address)
    contacts_id = create_contacts(conn, supplier_info.contacts)

    cur.callproc(
        'create_supplier', 
        (
            supplier_info.name, 
            contacts_id, 
            address_id
        )
    )

    supplier_id = cur.fetchone()
    cur.close()

    if supplier_id is None:
        raise UnableToCreateSupplier()

    return get_supplier(conn, supplier_id[0])
