import psycopg2.extras
import psycopg2
from app.schemas import Contact
from ._exceptions import ContactNotFound


def get_contact(conn: psycopg2.extensions.connection, contact_id: int):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.callproc('get_contact', (contact_id,))

    contact_data = cur.fetchone()

    if contact_data is None:
        raise ContactNotFound()

    contact = Contact(
        phone=contact_data[0],
        email=contact_data[1],
        telegram=contact_data[2]
    )

    conn.commit()
    cur.close()
    
    return contact