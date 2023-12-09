import psycopg2.extensions
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app import schemas
from app.usecases import customer, oauth2, supplier



class AccountAuthenticator:
    __auth_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def __init__(self, conn: psycopg2.extensions.connection):
        self._connection = conn

    def __call__(self, token: str = Depends(__auth_scheme)) -> schemas.Supplier | schemas.Customer:
        try:
            token_data = oauth2.decode_token(token)

            if token_data.type == "supplier":
                return supplier.get_supplier(self._connection, token_data.id)

            else:
                return customer.get_customer(self._connection, token_data.id)

        except:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
