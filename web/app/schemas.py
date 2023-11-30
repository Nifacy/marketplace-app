from pydantic import BaseModel, EmailStr, HttpUrl, validator
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


class ProductInfo(BaseModel):
    images: list[HttpUrl]
    price: float
    product_name: str
    description: str

    @validator('price')
    def validate_price(cls, v):
        if v < 0.0:
            raise ValueError("Price can't be neagtive or zero")
    
        if round(v, 2) != v:
            raise ValueError("Price must have max 2 digits after dot")
        
        return v
    
    @validator('product_name')
    def validate_product_name(cls, v):
        if len(v.splitlines()) > 1:
            raise ValueError("Product name can't be multiline")
        
        return v.strip()


class Product(BaseModel):
    id: int
    in_favorites: bool
    supplier: Supplier
    info: ProductInfo
    is_for_sale: bool
