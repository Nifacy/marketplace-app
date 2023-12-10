from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
import psycopg2.extensions

from . import database, schemas
from .usecases import customer, oauth2, supplier, product, favorites
from .dependencies import database, get_current_user


DependsDBConnection = Annotated[
    psycopg2.extensions.connection,
    Depends(database.get_connection),
]


DependsAuth = Annotated[
    schemas.Customer | schemas.Supplier,
    Depends(get_current_user),
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    database.open_connection()
    yield
    database.close_connection()


app = FastAPI(lifespan=lifespan)


@app.get("/supplier/me", response_model=schemas.Supplier)
async def get_current_supplier(user: DependsAuth):
    if not isinstance(user, schemas.Supplier):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@app.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier_endpoint(conn: DependsDBConnection, supplier_id: int):
    _supplier = supplier.get_supplier(conn, supplier_id)

    if not _supplier:
        raise HTTPException(status_code=404, detail=f"Supplier not found")

    return _supplier


@app.post("/supplier/register", response_model=schemas.Token)
async def register_supplier(conn: DependsDBConnection, register_form: schemas.SupplierRegisterForm):
    try:
        _supplier = supplier.register_supplier(conn, register_form)

        return schemas.Token(
            token=oauth2.generate_token(
                oauth2.TokenData(
                    type="supplier",
                    id=_supplier.id,
                ),
            ),
        )
    
    except supplier.SupplierAlreadyExists:
        raise HTTPException(status_code=409, detail="Supplier already exists")


@app.post("/supplier/login", response_model=schemas.Token)
async def login_supplier(conn: DependsDBConnection, credentials: schemas.SupplierCredentials):
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
async def register_customer(conn: DependsDBConnection, register_form: schemas.CustomerRegisterForm):
    try:
        _customer = customer.register_customer(conn, register_form)
        
        return schemas.Token(
            token=oauth2.generate_token(
                oauth2.TokenData(
                    type="customer",
                    id=_customer.id,
                ),
            ),
        )
    
    except customer.CustomerAlreadyExists:
        raise HTTPException(status_code=409, detail="Customer already exists")


@app.post("/customer/login", response_model=schemas.Token)
async def login_customer(conn: DependsDBConnection, credentials: schemas.CustomerCredentials):
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


@app.get("/customer/me", response_model=schemas.Customer)
async def get_current_customer(user: DependsAuth):
    if not isinstance(user, schemas.Customer):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@app.get("/customer/{id}", response_model=schemas.Customer)
async def get_customer_endpoint(conn: DependsDBConnection, id: int):
    try:
        return customer.get_customer(conn, id)
    except customer.CustomerNotFound:
        raise HTTPException(status_code=404, detail="Customer not found")


@app.get("/product")
async def get_products(conn: DependsDBConnection, user: DependsAuth, name: str | None = None) -> list[schemas.Product]:
    _products = product.get_products(conn, product.SearchFilters(name=name))
    
    if isinstance(user, schemas.Customer):
        favorite_products = favorites.get_favorites(conn, user.id)
        favorite_ids = set(p.id for p in favorite_products)
    else:
        favorite_ids = set()
    
    for p in _products:
        p.in_favorites = p.id in favorite_ids
    
    return _products


@app.get("/product/{id}", response_model=schemas.Product)
async def get_product_by_id(conn: DependsDBConnection, user: DependsAuth, id: int):
    _products = product.get_products(conn, product.SearchFilters(product_id=id))

    if len(_products) == 0:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    _product = _products[0]

    if isinstance(user, schemas.Customer):
        _product.in_favorites = _product.id in favorites.get_favorites(conn, user.id)
    
    return _products[0]
