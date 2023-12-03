from typing import Literal
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import ValidationError
from psycopg2.extensions import connection

from app.config import settings
from app.schemas import Customer, Supplier, TokenData
from .customer import get_customer
from .supplier import get_supplier
from ._exceptions import *


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_token(data: TokenData) -> str:
    to_encode = data.model_dump()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        token_type: Literal['supplier', 'customer'] | None = payload.get("type")
        id: str | None = payload.get("id")

        if token_type is None or id is None:
            raise UnableDecodeToken("Unable to decode token (None)")
        
        return TokenData(type=token_type, id=int(id))
    
    except JWTError:
        raise credentials_exception
    except ValidationError:
        raise UnableDecodeToken("Invalid token data")


def get_current_user(conn: connection, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)

    try:
        if token_data.type == 'supplier':
            user = get_supplier(conn, token_data.id)
        elif token_data.type == 'customer':
            user = get_customer(conn, token_data.id)
        else:
            raise HTTPException(status_code=400, detail="Invalid user type")
    except (SupplierNotFound, CustomerNotFound):
        raise credentials_exception

    return user
