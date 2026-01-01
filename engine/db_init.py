# engine/db_init.py

import sqlite3
from pathlib import Path
from engine.model_loader import load_models

DB_FILE = Path(__file__).parent / "app.db"

TYPE_MAP = {
    "integer": "INTEGER",
    "text": "TEXT",
    "float": "REAL",
    "boolean": "INTEGER",
    "enum": "TEXT",
}

def init_db():
    models = load_models()
    conn = sqlite3.connect(DB_FILE)

    for table_name, table_def in models.items():
        fields = table_def["fields"]

        columns = []
        for name, cfg in fields.items():
            col_type = TYPE_MAP[cfg["type"]]
            col_def = f"{name} {col_type}"
            if cfg.get("pk"):
                col_def += " PRIMARY KEY"
            if cfg.get("required"):
                col_def += " NOT NULL"
            columns.append(col_def)

        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {", ".join(columns)}
        );
        """
        conn.execute(sql)

    conn.commit()
    conn.close()
    print("✅ Database initialized")

if __name__ == "__main__":
    init_db()
