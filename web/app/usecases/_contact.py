import psycopg2.extras
import psycopg2
from app.schemas import Contact
from ._exceptions import ContactNotFound


def get_contact(conn: psycopg2.extensions.connection, contact_id: int) -> Contact:
    cur = conn.cursor()

    cur.callproc('get_contact', (contact_id,))

    contact_data = cur.fetchone()

    if contact_data is None:
        raise ContactNotFound()

    contact = Contact(
        phone=contact_data[1],
        email=contact_data[2],
        telegram=contact_data[3]
    )

    cur.close()

    return contact


def create_contact(conn: psycopg2.extensions.connection, contact: Contact) -> int:
    cur = conn.cursor()

    cur.callproc(
        'create_contact', 
        (
            contact.phone, 
            contact.email, 
            contact.telegram
            )
        )

    contact_id = cur.fetchone()[0]

    cur.close()

    return contact_id