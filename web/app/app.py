from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.database import connect
from app.schemas import Supplier
from app.usecases.usecases import get_supplier #, create_supplier


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
    global conn
    supplier = get_supplier(conn, supplier_id)
    
    if not supplier:
        raise HTTPException(status_code=404, detail=f'Supplier not found')
    
    return supplier
