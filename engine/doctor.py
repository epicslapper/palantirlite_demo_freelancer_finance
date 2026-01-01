# engine/doctor.py
"""
Project health check (read-only).

Checks:
- Database exists
- models.yaml loads
- Tables exist
- Columns match YAML
"""

from pathlib import Path
from engine.db import get_connection
from engine.model_loader import load_models

def main():
    print("🩺 Running PalantirLite doctor...\n")

    # ----------------------------
    # Check DB file
    # ----------------------------
    db_path = Path(__file__).parent / "app.db"
    assert db_path.exists(), f"❌ DB missing: {db_path}"
    print(f"✅ DB found: {db_path}")

    # ----------------------------
    # Load models.yaml
    # ----------------------------
    models = load_models()
    assert models, "❌ models.yaml empty or unreadable"
    print("✅ models.yaml loaded")

    conn = get_connection()

    for table_name, table_def in models.items():
        print(f"\n🔎 Checking table: {table_name}")

        # Table exists
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,),
        )
        assert cursor.fetchone(), f"❌ Table '{table_name}' missing"
        print("  ✅ table exists")

        # Columns match
        expected = set(table_def["fields"].keys())
        cursor = conn.execute(f"PRAGMA table_info({table_name});")
        actual = {row[1] for row in cursor.fetchall()}

        missing = expected - actual
        extra = actual - expected

        assert not missing, f"❌ Missing columns: {missing}"
        if extra:
            print(f"  ⚠️ Extra columns (allowed): {extra}")

        print("  ✅ columns OK")

    conn.close()
    print("\n🎉 Doctor check passed — system healthy")

if __name__ == "__main__":
    main()
