from typing import Literal
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings
from app.schemas import TokenData

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def generate_token(data: TokenData) -> str:
    to_encode = data.model_dump()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type: Literal['supplier', 'customer'] | None = payload.get("type")
        id: str | None = payload.get("id")
        if token_type is None or id is None:
            return None
        return TokenData(type=token_type, id=int(id))
    except JWTError:
        return None
