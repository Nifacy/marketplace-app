import psycopg2.extras
import psycopg2
from app.schemas import Product, ProductInfo
from ._exceptions import ProductNotFound, UnableToCreateProduct
from . import supplier


def get_product(conn: psycopg2.extensions.connection, product_id: int) -> Product:
    cur = conn.cursor()

    cur.callproc('get_product', (product_id,))
    response = cur.fetchone()
    
    if response is None:
        raise ProductNotFound()

    owner = supplier.get_supplier(conn, response[5])
    cur.close()

    return Product(
        id=response[0],
        in_favorites=False,
        info=ProductInfo(
            images=response[1],
            price=response[2],
            product_name=response[3],
            description=response[4],
            supplier=owner,
        ),
    )


def create_product(conn: psycopg2.extensions.connection, product_info: ProductInfo) -> Product:
    cur = conn.cursor()

    cur.callproc(
        'create_product', 
        (
            list(map(str, product_info.images)),
            product_info.product_name,
            product_info.price,
            product_info.description,
            product_info.supplier.id,
        )
    )

    product_id = cur.fetchone()
    cur.close()

    if product_id is None:
        raise UnableToCreateProduct()

    return get_product(conn, product_id[0])
