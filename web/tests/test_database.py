from app import database


def test_cancel_all_changes_after_closing_in_temporary_connection():
    for _ in range(2):
        conn = database.connect(database.temporary_connection)
        cur = conn.cursor()

        cur.execute("CREATE TABLE test_table (id serial PRIMARY KEY, num integer, data varchar);")

        cur.close()
        conn.close()


def test_storages_made_changes_per_session():
    conn = database.connect(database.temporary_connection)
    cur = conn.cursor()

    cur.execute("CREATE TABLE test_table (id serial PRIMARY KEY, num integer, data varchar);")
    cur.execute("INSERT INTO test_table (num, data) VALUES (%s, %s)", (100, "testdata"))

    cur.execute("SELECT * FROM test_table WHERE data='testdata';")
    record = cur.fetchone()
    
    assert record is not None
    assert record[1:] == (100, "testdata")

    cur.close()
    conn.close()
