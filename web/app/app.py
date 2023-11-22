from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from .database import connect
from .schemas import Supplier
from .usecases import get_supplier #, create_supplier


conn = None
@asynccontextmanager
async def lifespan(app: FastAPI):
    global conn
    conn = connect()
    yield
    conn.close()


app = FastAPI(lifespan=lifespan)


@app.get("/suppliers/{supplier_id}", response_model=Supplier)
async def get_supplier_endpoint(supplier_id: int):
    supplier = get_supplier(conn, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail=f'Supplier not found')
    return supplier
