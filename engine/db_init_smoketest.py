import sqlite3
from pathlib import Path

DB_FILE = Path("app.db")

def main():
    assert DB_FILE.exists(), "❌ app.db does not exist. Run db_init.py first."

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='tasks';"
    )
    table = cursor.fetchone()
    assert table is not None, "❌ Table 'tasks' does not exist."

    cursor = conn.execute("PRAGMA table_info(tasks);")
    columns = {row[1] for row in cursor.fetchall()}

    expected = {"id", "title", "priority", "done"}
    assert columns == expected, f"❌ Columns mismatch: {columns}"

    conn.close()
    print("✅ db_init smoketest passed")

if __name__ == "__main__":
    main()
