from typing import Literal
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import ValidationError
from app.config import settings
from app.schemas import TokenData
from ._exceptions import *


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


Token = str


def generate_token(data: TokenData) -> Token:
    to_encode = data.model_dump()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: Token) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        token_type: Literal['supplier', 'customer'] | None = payload.get("type")
        id: str | None = payload.get("id")

        if token_type is None or id is None:
            raise UnableDecodeToken("Unable to decode token (None)")
        
        return TokenData(type=token_type, id=int(id))
    
    except JWTError:
        raise UnableDecodeToken("Unable to decode token")
    except ValidationError:
        raise UnableDecodeToken("Invalid token data")
