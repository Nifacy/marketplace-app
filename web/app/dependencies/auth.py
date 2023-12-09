import psycopg2.extensions
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app import schemas
from app.usecases import customer, oauth2, supplier
from . import database


_auth_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    conn: psycopg2.extensions.connection = Depends(database.get_connection),
    token: oauth2.Token = Depends(_auth_scheme),
) -> schemas.Supplier | schemas.Customer:
    try:
        token_data = oauth2.decode_token(token)

        if token_data.type == "supplier":
            return supplier.get_supplier(conn, token_data.id)

        else:
            return customer.get_customer(conn, token_data.id)

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
