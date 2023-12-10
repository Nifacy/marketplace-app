import datetime
import itertools
import random
import string
from typing import Callable, TypeVar

from app import schemas
from pydantic import HttpUrl

_T = TypeVar('_T')

def _generate_password(length: int = 10):
    letter = random.choice(string.ascii_letters)
    digit = random.choice(string.digits)
    special_char = random.choice(string.punctuation)

    remaining_chars = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length - 3))
    password = letter + digit + special_char + remaining_chars
    password = ''.join(random.sample(password, len(password)))

    return password


# TODO: make type hints better here
def with_counter(func: Callable[..., _T]) -> Callable[..., _T]:
    _counter = itertools.count(start=1)
    def wrapper(*args, **kwargs) -> _T:
        count = next(_counter)
        return func(count, *args, **kwargs)
    return wrapper

@with_counter
def create_supplier_info_sample(count: int) -> schemas.SupplierInfo:
    return schemas.SupplierInfo(
        name=f'test-supplier-{count}',
        contacts=schemas.Contacts(
            phone='+1 (123) 456-7890',
            email='test.email@mail.com',
            telegram='@testsupplier',
        ),
        address=schemas.Address(
            street='Street',
            city='Moscow',
            country='Russia',
            postal_code='12345',
            house=1,
            entrance=1,
            appartment=1,
        )
    )

@with_counter
def create_customer_info_sample(count: int) -> schemas.CustomerInfo:
    return schemas.CustomerInfo(
        first_name=f'customer-{count}',
        last_name='last-name',
        contacts=schemas.Contacts(
            phone='+1 (123) 456-7890',
            email='test.email@mail.com',
            telegram='@testsupplier',
        ),
        address=schemas.Address(
            street='Street',
            city='Moscow',
            country='Russia',
            postal_code='12345',
            house=1,
            entrance=1,
            appartment=1,
        )
    )

@with_counter
def create_product_info_sample(count: int, **kwargs) -> schemas.ProductInfo:
    return schemas.ProductInfo(**{
        'images': [
            HttpUrl(f'http://example{count}.com'),
            HttpUrl(f'http://example{count + 1}.com'),
        ],
        'price': 100.82,
        'product_name': f'Product #{count}',
        'description': 'some description here...',
        **kwargs
    })

@with_counter
def create_address_sample(count: int) -> schemas.Address:
    return schemas.Address(
        street=f'Street {count}',
        city='City',
        country='Country',
        postal_code='12345',
        house=count,
        entrance=1,
        appartment=1,
    )

@with_counter
def create_customer_register_form(count: int) -> schemas.CustomerRegisterForm:
    supplier_info = create_customer_info_sample()
    customer_credentials = schemas.CustomerCredentials(
        login=f"test-supplier-{count}",
        password=_generate_password(),
    )
    return schemas.CustomerRegisterForm(
        credentials=customer_credentials,
        info=supplier_info,
    )

@with_counter
def create_supplier_register_form(count: int) -> schemas.SupplierRegisterForm:
    supplier_info = create_supplier_info_sample()
    customer_credentials = schemas.SupplierCredentials(
        login=f"test-supplier-{count}",
        password=_generate_password(),
    )
    return schemas.SupplierRegisterForm(
        credentials=customer_credentials,
        info=supplier_info,
    )
