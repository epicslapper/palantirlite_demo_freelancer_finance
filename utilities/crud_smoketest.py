import streamlit as st
from engine.db import get_connection
from engine.model_loader import load_models


# i thinkw we are missing the simple delete ?? remebmer we DO NOT use soft delete anymore !!!

from engine.crud import (
    fetch_active_rows,
    insert_row,
    update_row
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

conn.close()
