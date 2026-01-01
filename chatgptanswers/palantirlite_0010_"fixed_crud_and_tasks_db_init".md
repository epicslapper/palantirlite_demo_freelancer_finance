palantirlite_0009_"fixed_crud_and_tasks_db_init".md

You are **100% right** to call out the rule — good catch 👍
Let’s proceed **cleanly, deterministically, and slowly**.

We will do **exactly** what you asked, nothing more:

1. Re-establish the **tiny `tasks` test app**
2. Define the **`models.yaml` contract**
3. Create a **new `db_init.py`**
4. Answer the **important architectural question**:

   > *Is `db_init.py` agnostic / stable / “never changed again”?*

---

## 1️⃣ The tiny `tasks` model (ground truth)

This is the **only source of truth** for schema intent.

```yaml
# models.yaml
tasks:
  fields:
    id:
      type: integer
      pk: true
      editable: false

    title:
      type: text
      required: true

    priority:
      type: enum
      values: [low, medium, high]

    done:
      type: boolean
```

### Important notes (intentional design)

* `editable: false`
  → **engine ignores this**
  → UI / app layer may use it later
  → engine stays boring

* `enum.values`
  → stored as TEXT in SQLite
  → meaning is meta-level, not enforced in DB

Perfect.

---

## 2️⃣ Role of `db_init.py` (very important)

Before writing code, let’s **lock the philosophy**, otherwise this will rot.

### `db_init.py` has ONE job

> **Materialize YAML → SQLite schema**

That’s it.

It is **NOT**:

* a migration tool
* a schema editor
* a business rules engine
* a validator
* a UI helper

---

## 3️⃣ Should `db_init.py` be agnostic & never changed?

### Short answer

**Yes — conceptually.
No — practically (but very rarely).**

### The correct mental model

`db_init.py` is like:

* `terraform init`
* `make bootstrap`
* `db create`

You may:

* add support for *new YAML features* (once every few months)
* extend type mappings (rare)

You should **not**:

* tweak it per project
* add business logic
* add hacks for one client

If you feel the urge → the design is wrong.

---

## 4️⃣ New clean `engine/db_init.py`

This version is:

* fully agnostic
* deterministic
* safe
* aligned with your rules
* **boring by design**

### `engine/db_init.py`

```python
# ----------------------------
# FILE: engine/db_init.py
# ----------------------------
"""
Initialize SQLite database from models.yaml.

Responsibilities:
- Create tables if they do not exist
- Ensure columns defined in YAML exist
- NO data migration
- NO destructive changes (no DROP)
- NO business logic

This file is intentionally boring.
"""

import sqlite3
import yaml
from pathlib import Path

DB_FILE = Path("app.db")
MODEL_FILE = Path("models.yaml")

# YAML → SQLite type mapping
TYPE_MAP = {
    "integer": "INTEGER",
    "text": "TEXT",
    "float": "REAL",
    "boolean": "INTEGER",
    "enum": "TEXT",
}

def load_models():
    with open(MODEL_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_existing_columns(conn, table_name):
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}

def create_table_if_missing(conn, table_name, fields):
    columns_sql = []

    for field_name, cfg in fields.items():
        col_type = TYPE_MAP.get(cfg["type"], "TEXT")
        col_def = f"{field_name} {col_type}"

        if cfg.get("pk"):
            col_def += " PRIMARY KEY"
        if cfg.get("required"):
            col_def += " NOT NULL"

        columns_sql.append(col_def)

    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {", ".join(columns_sql)}
    );
    """

    conn.execute(sql)

def add_missing_columns(conn, table_name, fields):
    existing_cols = get_existing_columns(conn, table_name)

    for field_name, cfg in fields.items():
        if field_name in existing_cols:
            continue

        col_type = TYPE_MAP.get(cfg["type"], "TEXT")
        sql = f"ALTER TABLE {table_name} ADD COLUMN {field_name} {col_type}"
        conn.execute(sql)

def init_db():
    models = load_models()
    conn = sqlite3.connect(DB_FILE)

    for table_name, table_def in models.items():
        fields = table_def.get("fields", {})
        create_table_if_missing(conn, table_name, fields)
        add_missing_columns(conn, table_name, fields)

    conn.commit()
    conn.close()

    print("Database initialized (add-only, non-destructive).")

if __name__ == "__main__":
    init_db()
```

---

## 5️⃣ Why this design is correct (important)

### What it guarantees

✅ Idempotent (run it 100 times)
✅ Add-only
✅ No silent drops
✅ YAML remains the authority
✅ Safe for demos AND production

---

### What it deliberately avoids

❌ DROP TABLE
❌ ALTER COLUMN
❌ ENUM enforcement
❌ Defaults
❌ Data rewriting

Those belong to:

* migration tools
* derived layers
* explicit human decisions

---

## 6️⃣ How this fits with `crud.py`

This is the key abstraction boundary:

| Layer             | Responsibility       |
| ----------------- | -------------------- |
| `db_init.py`      | *structure exists*   |
| `crud.py`         | *rows move in/out*   |
| `schema_check.py` | *truth comparison*   |
| app / Streamlit   | *meaning & workflow* |

No overlaps.
No cleverness.
No surprises.

---

## 7️⃣ Next **small** step (recommended)

Before UI, before AI:

👉 **Write `tasks_app.py` (10–20 lines)**

* list tasks
* add task
* mark done

Using:

* `crud.py`
* `models.yaml`
* `db_init.py`

This will prove the stack is **alive**, not theoretical.

When you say the word, we’ll build that next — slowly, cleanly, and auditable.

palantirlite_0009_"fixed_crud_and_tasks_db_init".md

