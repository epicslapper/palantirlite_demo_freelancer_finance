# ----------------------------
# FILE: init_db.py
# ----------------------------
import sqlite3
import yaml
from pathlib import Path

DB_FILE = Path("app.db")
MODEL_FILE = Path("models.yaml")

# ----------------------------
# Load model
# ----------------------------
with open(MODEL_FILE) as f:
    models = yaml.safe_load(f)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

TYPE_MAP = {
    "integer": "INTEGER",
    "text": "TEXT",
    "float": "REAL",
    "boolean": "INTEGER",
    "enum": "TEXT",
}

for table_name, table in models.items():
    # get existing columns
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_columns = [row[1] for row in cursor.fetchall()]
    yaml_columns = list(table["fields"].keys())

    if set(existing_columns) != set(yaml_columns):
        print(f"Schema mismatch detected for table '{table_name}', recreating...")
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # create table
    columns = []
    for field, cfg in table["fields"].items():
        col_type = TYPE_MAP.get(cfg["type"], "TEXT")
        col_def = f"{field} {col_type}"
        if cfg.get("pk"):
            col_def += " PRIMARY KEY"
        if cfg.get("required"):
            col_def += " NOT NULL"
        columns.append(col_def)

    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
    print(sql)
    cursor.execute(sql)

conn.commit()
conn.close()
print("Database initialized and synced with YAML model.")
