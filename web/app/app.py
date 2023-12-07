from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from . import database
from . import schemas
from .usecases import supplier
from .usecases import oauth2

conn = None

@asynccontextmanager
async def lifespan(_: FastAPI):
    global conn
    conn = database.connect(database.from_settings)
    yield
    conn.close()


app = FastAPI(lifespan=lifespan)


@app.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier_endpoint(supplier_id: int):
    global conn
    _supplier = supplier.get_supplier(conn, supplier_id)

    if not _supplier:
        raise HTTPException(status_code=404, detail=f'Supplier not found')

    return _supplier


@app.post("/supplier/register", response_model=schemas.Token)
async def register_supplier(register_form: schemas.SupplierRegisterForm):
    global conn
    _supplier = supplier.register_supplier(conn, register_form)
    return schemas.Token(
        token=oauth2.generate_token(oauth2.TokenData(
            type='supplier',
            id=_supplier.id
        )),
    )
