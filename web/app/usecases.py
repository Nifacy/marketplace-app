import psycopg2
from .schemas import Supplier


class SupplierNotFound(Exception):
    pass


def create_supplier(conn: psycopg2.extensions.connection, supplier: Supplier) -> None:
    cur = conn.cursor()

    args = {**supplier.model_dump(), **supplier.address.model_dump()}
    args.pop('address')

    cur.callproc('sql.add_supplier', tuple(args.values()))

    conn.commit()
    cur.close()


def get_supplier(conn: psycopg2.extensions.connection, supplier_id: int) -> Supplier:
    cur = conn.cursor()

    cur.callproc('sql.get_supplier', (supplier_id,))

    supplier = cur.fetchone()

    conn.commit()
    cur.close()

    if supplier is None:
        raise SupplierNotFound()

    return Supplier(**supplier)