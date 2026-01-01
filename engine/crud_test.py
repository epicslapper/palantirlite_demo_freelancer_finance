import sqlite3
from engine.crud import fetch_rows, insert_row, update_row, delete_row

DB_FILE = "crud_test.db"
TABLE = "test_items"

def setup_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            value INTEGER
        )
    """)
    conn.commit()
    return conn

def run_test():
    conn = setup_db()

    print("1. Insert row")
    insert_row(conn, TABLE, {"name": "alpha", "value": 10})

    rows = fetch_rows(conn, TABLE)
    assert len(rows) == 1
    row_id = int(rows.iloc[0]["id"])

    print("2. Update row")
    update_row(conn, TABLE, row_id, {"value": 20})

    rows = fetch_rows(conn, TABLE)
    assert rows.iloc[0]["value"] == 20

    print("3. Delete row")
    delete_row(conn, TABLE, row_id)

    rows = fetch_rows(conn, TABLE)
    assert len(rows) == 0

    conn.close()
    print("CRUD test PASSED")

if __name__ == "__main__":
    run_test()
