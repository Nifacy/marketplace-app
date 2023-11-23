import psycopg2.extras
import psycopg2
from app.schemas import Supplier
from ._exceptions import *
from ._address import get_address
from ._contact import get_contact


def get_supplier(conn: psycopg2.extensions.connection, supplier_id: int):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.callproc('get_supplier', (supplier_id,))
    # 0 - id; 1 - name; 2 - contact; 3 - address
    supplier = cur.fetchone()
    contact = get_contact(conn, supplier[2])
    address = get_address(conn, supplier[3])

    if supplier is None:
        raise SupplierNotFound()
    
    print(contact)
    print(address)
    print(supplier)

    conn.commit()
    cur.close()
    return supplier