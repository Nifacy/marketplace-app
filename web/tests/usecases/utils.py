import itertools
from typing import Callable, TypeVar
from app.schemas import Address, Contacts, SupplierInfo, CustomerInfo

_T = TypeVar('_T')

# TODO: make type hints better here
def with_counter(func: Callable[..., _T]) -> Callable[..., _T]:
    _counter = itertools.count(start=1)
    def wrapper(*args, **kwargs) -> _T:
        count = next(_counter)
        return func(count, *args, **kwargs)
    return wrapper

@with_counter
def create_supplier_info_sample(count: int) -> SupplierInfo:
    return SupplierInfo(
        name=f'test-supplier-{count}',
        contacts=Contacts(
            phone='+1 (123) 456-7890',
            email='test.email@mail.com',
            telegram='@testsupplier',
        ),
        address=Address(
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
def create_customer_info_sample(count: int) -> CustomerInfo:
    return CustomerInfo(
        first_name=f'customer-{count}',
        last_name='last-name',
        contacts=Contacts(
            phone='+1 (123) 456-7890',
            email='test.email@mail.com',
            telegram='@testsupplier',
        ),
        address=Address(
            street='Street',
            city='Moscow',
            country='Russia',
            postal_code='12345',
            house=1,
            entrance=1,
            appartment=1,
        )
    )
