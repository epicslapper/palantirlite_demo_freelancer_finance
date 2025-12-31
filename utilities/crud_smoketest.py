import streamlit as st
from engine.db import get_connection
from engine.model_loader import load_models
from engine.crud import (
    fetch_active_rows,
    fetch_deleted_rows,
    insert_row,
    update_row,
    soft_delete_row,
    restore_row,
)

st.title("CRUD Smoke Test")

models = load_models("models.yaml")
table_name = list(models.keys())[0]

# ----------------------------
# Connect to DB
# ----------------------------
conn = get_connection()

# ----------------------------
# 1. Insert test row
# ----------------------------
test_data = {"title": "SmokeTest Task", "priority": "medium", "done": 0}
insert_row(conn, table_name, test_data)
st.success("✅ Test row inserted")

# ----------------------------
# 2. Fetch active rows
# ----------------------------
active = fetch_active_rows(conn, table_name)
st.write("Active rows after insert:", active)

# ----------------------------
# 3. Update row
# ----------------------------
if not active.empty:
    first_id = int(active.iloc[0]["id"])
    update_row(conn, table_name, first_id, {"title": "Updated SmokeTest"})
    st.success(f"✅ Row {first_id} updated")

    updated_active = fetch_active_rows(conn, table_name)
    st.write("Active rows after update:", updated_active)

# ----------------------------
# 4. Soft-delete row
# ----------------------------
if not active.empty:
    soft_delete_row(conn, table_name, first_id)
    st.success(f"✅ Row {first_id} soft-deleted")

    after_delete = fetch_active_rows(conn, table_name)
    deleted_rows = fetch_deleted_rows(conn, table_name)
    st.write("Active rows after soft-delete:", after_delete)
    st.write("Deleted rows:", deleted_rows)

# ----------------------------
# 5. Restore row
# ----------------------------
if not deleted_rows.empty:
    restore_row(conn, table_name, first_id)
    st.success(f"✅ Row {first_id} restored")

    final_active = fetch_active_rows(conn, table_name)
    st.write("Active rows after restore:", final_active)

conn.close()
