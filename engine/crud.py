# ----------------------------
# FILE: engine/crud.py
# ----------------------------
import pandas as pd

# ----------------------------
# Fetch rows
# ----------------------------
def fetch_active_rows(conn, table_name):
    """Return all rows in the table"""
    return pd.read_sql(
        f"SELECT * FROM {table_name}",
        conn
    )

# ----------------------------
# Insert / Update / Delete
# ----------------------------
def insert_row(conn, table_name, data):
    """Insert a row into table"""
    keys = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    values = list(data.values())

    conn.execute(
        f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})",
        values
    )
    conn.commit()

def update_row(conn, table_name, row_id, data):
    """Update row by ID"""
    sets = ", ".join([f"{k}=?" for k in data.keys()])
    values = list(data.values()) + [row_id]

    conn.execute(
        f"UPDATE {table_name} SET {sets} WHERE id=?",
        values
    )
    conn.commit()

def delete_row(conn, table_name, row_id):
    """Delete row by ID"""
    conn.execute(
        f"DELETE FROM {table_name} WHERE id=?",
        (row_id,)
    )
    conn.commit()
