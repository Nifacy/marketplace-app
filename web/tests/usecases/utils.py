import itertools
from typing import Callable, TypeVar
from app import schemas

_T = TypeVar('_T')

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
def create_product_info_sample(count: int, supplier: schemas.Supplier, **kwargs) -> schemas.ProductInfo:
    return schemas.ProductInfo(**{
        'images': [
            f'http://example{count}.com',
            f'http://example{count + 1}.com',
        ],
        'price': 100.82,
        'product_name': f'Product #{count}',
        'description': 'some description here...',
        'supplier': supplier,
        **kwargs
    })
