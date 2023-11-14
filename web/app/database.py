import psycopg2

# зуй хуй хуй хуй
conn = None

def initialize_database():
    global conn
    conn = psycopg2.connect(
        dbname="наша-дбшка",
        user="пидорас",
        password="MyWifeLeftMe;(",
        host="localhost"
    )

    # Инициализация базы данных
    cur = conn.cursor()
    with open('sql/initialise.sql', 'r') as f:
        cur.execute(f.read())
    conn.commit()

def close_database():
    global conn
    conn.close()