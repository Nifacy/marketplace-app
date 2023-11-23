from pydantic import BaseModel, EmailStr, validator
import re

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str
    house: int
    entrance: int | None = None
    appartment: int | None = None

class Contacts(BaseModel):
    phone: str
    email: EmailStr
    telegram: str | None = None

    @validator('phone')
    def validate_phone(cls, v):
        pattern = r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number')
        return v

    @validator('telegram')
    def validate_telegram(cls, v):
        pattern = r'^@[a-zA-Z0-9_]{5,}$'
        if v is not None and not re.match(pattern, v):
            raise ValueError('Invalid telegram handle')
        return v


class SupplierInfo(BaseModel):
    name: str
    contacts: Contacts
    address: Address


class Supplier(BaseModel):
    id: int
    info: SupplierInfo


class CustomerInfo(BaseModel):
    first_name: str
    last_name: str
    contacts: Contacts
    address: Address


class Customer(BaseModel):
    id: int
    info: CustomerInfo