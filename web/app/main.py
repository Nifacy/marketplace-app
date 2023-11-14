from fastapi import FastAPI, HTTPException
from .database import initialize_database, close_database
from .schemas import Supplier
import psycopg2


app = FastAPI()
conn = None # она ещё в database.py есть
# Я не понял рофла, куда её кидать, так что я в оба добавил, питон сложный аааааааа
# мб импортить надо, но я не хочу пачкаться


@app.router.on_startup
async def startup():
    global conn
    conn = initialize_database()


@app.router.on_shutdown
async def shutdown():
    close_database()


# хз, пример, как эта шняга выглядить может, скажи, норм/не норм
# я перекину это в routers, очев, но пока здесь, чтоб посмотреть
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

    return Supplier(**supplier)


@app.post("/suppliers/", response_model=Supplier)
async def create_supplier_endpoint(supplier: Supplier):
    try:
        create_supplier(conn, supplier)
    # Я только хз, насчет формата исключений, аааааа
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return supplier.model_dump()

@app.get("/suppliers/{supplier_id}", response_model=Supplier)
async def get_supplier_endpoint(supplier_id: int):
    try:
        supplier = get_supplier(conn, supplier_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

