import psycopg2.extras
import psycopg2
from app.schemas import Contacts
from ._exceptions import ContactsNotFound, UnableToCreateContacts


def get_contacts(conn: psycopg2.extensions.connection, contacts_id: int) -> Contacts:
    cur = conn.cursor()

    cur.callproc('get_contacts', (contacts_id,))

    contacts_data = cur.fetchone()

    if contacts_data is None:
        raise ContactsNotFound()

    contacts = Contacts(
        phone=contacts_data[1],
        email=contacts_data[2],
        telegram=contacts_data[3]
    )

    cur.close()

    return contacts


def create_contacts(conn: psycopg2.extensions.connection, contacts: Contacts) -> int:
    cur = conn.cursor()

    cur.callproc(
        'create_contacts', 
        (
            contacts.phone, 
            contacts.email, 
            contacts.telegram
        )
    )

    response = cur.fetchone()
    if response is None:
        raise UnableToCreateContacts()

    contacts_id = response[0]
    cur.close()

    return contacts_id
