# engine/yaml_sanity_check.py
"""
YAML-driven sanity check.

- Uses models.yaml as source of truth
- Validates DB schema
- Tests CRUD wiring
- No Streamlit
- Generic across all projects
"""

from engine.db import get_connection
from engine.crud import insert_row, fetch_rows, update_row
from engine.model_loader import load_models

def build_minimal_payload(fields: dict) -> dict:
    """
    Create a minimal valid insert payload from YAML fields.
    """
    payload = {}

    for name, cfg in fields.items():
        if cfg.get("pk"):
            continue

        field_type = cfg["type"]

        if field_type == "integer":
            payload[name] = 0
        elif field_type == "float":
            payload[name] = 0.0
        elif field_type == "boolean":
            payload[name] = 0
        elif field_type == "enum":
            payload[name] = cfg["values"][0]
        else:
            payload[name] = "sanity"

    return payload

def sanity_check_from_yaml():
    models = load_models()
    conn = get_connection()

    for table_name, table_def in models.items():
        print(f"\n🔎 Checking table: {table_name}")

        fields = table_def["fields"]
        expected_columns = set(fields.keys())

        # ----------------------------
        # Check table exists
        # ----------------------------
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,),
        )
        assert cursor.fetchone(), f"❌ Table '{table_name}' missing"

        # ----------------------------
        # Check columns
        # ----------------------------
        cursor = conn.execute(f"PRAGMA table_info({table_name});")
        actual_columns = {row[1] for row in cursor.fetchall()}
        missing = expected_columns - actual_columns
        assert not missing, f"❌ Missing columns in {table_name}: {missing}"

        # ----------------------------
        # Insert minimal row
        # ----------------------------
        payload = build_minimal_payload(fields)
        insert_row(conn, table_name, payload)

        # ----------------------------
        # Fetch rows
        # ----------------------------
        df = fetch_rows(conn, table_name)
        assert not df.empty, f"❌ No rows returned from {table_name}"

        print(f"✅ Table '{table_name}' passed")

    conn.close()
    print("\n🎉 All YAML sanity checks passed")

if __name__ == "__main__":
    sanity_check_from_yaml()
