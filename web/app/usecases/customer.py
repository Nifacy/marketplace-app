from psycopg2.extensions import connection
from app.schemas import Customer, CustomerCredentials, CustomerInfo, CustomerRegisterForm
from ._exceptions import *
from ._address import get_address, create_address
from ._contacts import get_contacts, create_contacts


SUCCESS_REGISTRATION = 'Customer registration successful'

def get_customer(conn: connection, customer_id: int) -> Customer:
    cur = conn.cursor()

    cur.callproc('get_customer', (customer_id,))

    # 0 - id; 1 - first_name; 2 - last_name; 3 - contacts; 4 - address
    customer_data = cur.fetchone()

    if customer_data is None:
        raise CustomerNotFound()

    contacts = get_contacts(conn, customer_data[3])
    address = get_address(conn, customer_data[4])
    
    customer_info = CustomerInfo(
        first_name=customer_data[1],
        last_name=customer_data[2],
        contacts=contacts,
        address=address
    )
    customer = Customer(
        id=customer_data[0],
        info=customer_info
    )

    cur.close()

    return customer


def create_customer(conn: connection, customer_info: CustomerInfo) -> Customer:
    cur = conn.cursor()

    address_id = create_address(conn, customer_info.address)
    contacts_id = create_contacts(conn, customer_info.contacts)

    cur.callproc(
        'create_customer', 
        (
            customer_info.first_name, 
            customer_info.last_name, 
            contacts_id, 
            address_id
        )
    )

    response = cur.fetchone()
    cur.close()

    if response is None:
        raise UnableToCreateCustomer()
    
    return get_customer(conn, response[0])


def register_customer(conn: connection, customer_form: CustomerRegisterForm) -> Customer:
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM customer_credentials WHERE login = %s", (customer_form.credentials.login,))
    if cur.fetchone()[0] > 0:
        raise CustomerAlreadyExists()
    
    customer = create_customer(conn, customer_form.info)

    cur.callproc(
        'register_customer', 
        (customer_form.credentials.login, 
         customer_form.credentials.password, 
         customer.id
        )
    )
    
    message = cur.fetchone()[0]
    if message != SUCCESS_REGISTRATION:
        cur.callproc('delete_customer_upon_registration', (customer.id,))
        raise UnableToCreateCustomer()
    
    cur.close()
    return customer



def login_customer(conn: connection, credentials: CustomerCredentials) -> Customer:
    cur = conn.cursor()
    
    cur.callproc(
        'login_customer', 
        (
            credentials.login, 
            credentials.password
        )
    )

    customer_id = cur.fetchone()[0]
    cur.close()
    
    if customer_id is None:
        raise InvalidCredentials()
    
    return get_customer(conn, customer_id)