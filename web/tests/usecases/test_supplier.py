import pytest

from app.usecases import supplier
from . import utils


def test_supplier_creation(db_connection):
    supplier_info_sample = utils.create_supplier_info_sample()
    created_supplier = supplier.create_supplier(db_connection, supplier_info_sample)

    assert created_supplier.info == supplier_info_sample


def test_supplier_getable_after_creation(db_connection):
    supplier_info_sample = utils.create_supplier_info_sample()
    created_supplier = supplier.create_supplier(db_connection, supplier_info_sample)
    found_supplier = supplier.get_supplier(db_connection, created_supplier.id)

    assert created_supplier == found_supplier


def test_supplier_not_found(db_connection):
    with pytest.raises(supplier.SupplierNotFound):
        supplier.get_supplier(db_connection, 1)

    db_connection.close()
