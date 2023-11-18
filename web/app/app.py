from fastapi import FastAPI, HTTPException
from .database import connect
from .schemas import Supplier
from .usecases import get_supplier #, create_supplier

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

# TODO: check if can be changed to be used, and remove if not
# @app.post("/suppliers/", response_model=Supplier)
# async def create_supplier_endpoint(supplier: Supplier):
#     try:
#         create_supplier(conn, supplier)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

#     return supplier


@app.get("/suppliers/{supplier_id}", response_model=Supplier)
async def get_supplier_endpoint(supplier_id: int):
    supplier = get_supplier(conn, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail=f'Supplier not found')
    return supplier
