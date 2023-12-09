from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from . import database, schemas
from .usecases import customer, oauth2, supplier

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
        raise HTTPException(status_code=404, detail=f"Supplier not found")

    return _supplier


@app.post("/supplier/register", response_model=schemas.Token)
async def register_supplier(register_form: schemas.SupplierRegisterForm):
    global conn
    _supplier = supplier.register_supplier(conn, register_form)
    return schemas.Token(
        token=oauth2.generate_token(
            oauth2.TokenData(
                type="supplier",
                id=_supplier.id,
            ),
        ),
    )


@app.post("/supplier/login", response_model=schemas.Token)
async def login_supplier(credentials: schemas.SupplierCredentials):
    global conn

    try:
        _supplier = supplier.login_supplier(conn, credentials)

        return schemas.Token(
            token=oauth2.generate_token(
                oauth2.TokenData(
                    type="supplier",
                    id=_supplier.id,
                ),
            ),
        )

    except supplier.InvalidCredentials:
        raise HTTPException(
            status_code=401,
            detail="Wrong login or password",
        )


@app.post("/customer/register", response_model=schemas.Token)
async def register_customer(register_form: schemas.CustomerRegisterForm):
    global conn
    _customer = customer.register_customer(conn, register_form)
    return schemas.Token(
        token=oauth2.generate_token(
            oauth2.TokenData(
                type="customer",
                id=_customer.id,
            ),
        ),
    )


@app.post("/customer/login", response_model=schemas.Token)
async def login_customer(credentials: schemas.CustomerCredentials):
    global conn

    try:
        _customer = customer.login_customer(conn, credentials)

        return schemas.Token(
            token=oauth2.generate_token(
                oauth2.TokenData(
                    type="customer",
                    id=_customer.id,
                )
            )
        )

    except supplier.InvalidCredentials:
        raise HTTPException(
            status_code=401,
            detail="Wrong login or password",
        )
