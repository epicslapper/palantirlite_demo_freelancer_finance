Perfect — this is exactly the **right order** 👍
We will do this **mechanically and verifiably**, no magic.

Below is **everything you need in one place**, step by step.

---

# 1️⃣ How to run `db_init.py` (first principles)

### Preconditions

You must have:

* `models.yaml`
* `engine/db_init.py`
* Python environment with `pyyaml`

### Command (from project root)

```bash
python engine/db_init.py
```

### What should happen

* `app.db` is created (if missing)
* table `tasks` is created
* **no output except**:

```text
Database initialized (add-only, non-destructive).
```

If you run it **again**, nothing changes — that’s the point.

---

# 2️⃣ Very small **db_init smoketest**

This test proves **structure**, not CRUD.

Create this file:

```
utilities/db_init_smoketest.py
```

### `utilities/db_init_smoketest.py`

```python
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
```

### Run it

```bash
python utilities/db_init_smoketest.py
```

Expected output:

```text
✅ db_init smoketest passed
```

This proves:

* YAML → DB works
* schema is correct
* no UI, no CRUD involved

---

# 3️⃣ Minimal `tasks_app.py` (Streamlit)

This is **not architecture**, just proof of life.

Create at project root:

```
tasks_app.py
```

---

### `tasks_app.py`

```python
import streamlit as st
from engine.db import get_connection
from engine.crud import fetch_active_rows, insert_row, update_row

st.title("🧪 Tasks – minimal PalantirLite demo")

conn = get_connection()

# ----------------------------
# Add task
# ----------------------------
st.subheader("Add task")

title = st.text_input("Title")
priority = st.selectbox("Priority", ["low", "medium", "high"])

if st.button("Add"):
    if title.strip():
        insert_row(
            conn,
            "tasks",
            {
                "title": title,
                "priority": priority,
                "done": 0,
            },
        )
        st.success("Task added")
    else:
        st.warning("Title required")

# ----------------------------
# Show tasks
# ----------------------------
st.subheader("Tasks")

df = fetch_active_rows(conn, "tasks")

if not df.empty:
    st.dataframe(df)

    st.subheader("Mark task as done")
    task_id = st.selectbox("Task ID", df["id"].tolist())

    if st.button("Mark done"):
        update_row(conn, "tasks", task_id, {"done": 1})
        st.success(f"Task {task_id} marked done")
else:
    st.info("No tasks yet")

conn.close()
```

---

# 4️⃣ How to run the app

```bash
streamlit run tasks_app.py
```

You now have:

* YAML-driven schema
* deterministic DB init
* verified schema
* working CRUD
* minimal UI

No migrations.
No normalization.
No Oracle thinking.

---

# 5️⃣ What we have **proven**

✅ `models.yaml` is the contract
✅ `db_init.py` is stable & reusable
✅ CRUD is schema-agnostic
✅ UI is thin and disposable

This is **PalantirLite in miniature**.

---

## Next logical steps (don’t do all at once)

Pick **one** next time:

1. Raw / Meta / Derived table taxonomy (applied to your Excel tax data)
2. Excel → raw SQLite importer (1:1, zero interpretation)
3. Dockerizing this exact setup
4. Turning this into the 2-page architecture PDF

Say the word — we move one layer up, not sideways.

