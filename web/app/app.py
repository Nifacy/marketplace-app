from fastapi import FastAPI, HTTPException
from .database import connect
from .schemas import Supplier
import psycopg2


class SupplierNotFound(Exception):
    pass


app = FastAPI()
conn = None


@app.router.on_startup
async def startup():
    global conn
    conn = connect()


@app.router.on_shutdown
async def shutdown():
    global conn
    conn.close()


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



@app.post("/suppliers/", response_model=Supplier)
async def create_supplier_endpoint(supplier: Supplier):
    try:
        create_supplier(conn, supplier)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return supplier


@app.get("/suppliers/{supplier_id}", response_model=Supplier)
async def get_supplier_endpoint(supplier_id: int):
    supplier = get_supplier(conn, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail=f'Supplier not found')
    return supplier
