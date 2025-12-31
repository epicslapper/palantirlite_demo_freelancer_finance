# engine/schema_check.py
"""
READ-ONLY schema checker.
Compares models.yaml against actual SQLite schema.
NO writes. NO migrations. NO side effects.
"""

import sqlite3


SQLITE_TYPE_MAP = {
    "integer": "INTEGER",
    "text": "TEXT",
    "float": "REAL",
    "boolean": "INTEGER",
    "enum": "TEXT",   # enums stored as TEXT in SQLite
}


def get_db_schema(conn, table_name: str) -> dict:
    """
    Returns DB schema as:
    {
        column_name: {
            "type": "TEXT",
            "pk": True/False,
            "notnull": True/False
        }
    }
    """
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    schema = {}

    for cid, name, coltype, notnull, default, pk in cursor.fetchall():
        schema[name] = {
            "type": coltype.upper(),
            "pk": bool(pk),
            "notnull": bool(notnull),
        }

    return schema


def check_table_schema(conn, table_name: str, yaml_fields: dict) -> list[str]:
    """
    Compares YAML table definition to DB table.
    Returns list of human-readable messages.
    """
    messages = []

    # --- check table exists
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    if cursor.fetchone() is None:
        messages.append(f"❌ Table '{table_name}' does NOT exist in DB.")
        return messages

    messages.append(f"✔ Table '{table_name}' exists.")

    db_schema = get_db_schema(conn, table_name)

    yaml_columns = set(yaml_fields.keys())
    db_columns = set(db_schema.keys())

    # --- missing columns
    for col in yaml_columns - db_columns:
        messages.append(f"❌ Missing column in DB: '{col}'")

    # --- extra columns
    for col in db_columns - yaml_columns:
        messages.append(f"⚠ Extra column in DB not in YAML: '{col}'")

    # --- compare shared columns
    for col in yaml_columns & db_columns:
        yaml_cfg = yaml_fields[col]
        db_col = db_schema[col]

        expected_type = SQLITE_TYPE_MAP.get(yaml_cfg["type"], "TEXT")

        if db_col["type"] != expected_type:
            messages.append(
                f"⚠ Column '{col}' type mismatch: DB={db_col['type']} YAML={expected_type}"
            )

        if yaml_cfg.get("pk", False) != db_col["pk"]:
            messages.append(
                f"⚠ Column '{col}' PK mismatch: DB={db_col['pk']} YAML={yaml_cfg.get('pk', False)}"
            )

        if yaml_cfg.get("required", False) != db_col["notnull"]:
            messages.append(
                f"⚠ Column '{col}' NULL constraint mismatch: DB notnull={db_col['notnull']} YAML required={yaml_cfg.get('required', False)}"
            )

    if len(messages) == 1:
        messages.append("✔ Schema fully matches YAML.")

    return messages


def check_schema(conn, models: dict) -> dict:
    """
    Checks all tables defined in models.yaml.
    Returns dict:
    {
        table_name: [messages]
    }
    """
    report = {}

    for table_name, table_def in models.items():
        fields = table_def.get("fields", {})
        report[table_name] = check_table_schema(conn, table_name, fields)

    return report
