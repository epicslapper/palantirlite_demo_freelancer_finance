import streamlit as st
import pandas as pd
from engine.db import get_connection
from engine.crud import fetch_rows, insert_row, update_row, delete_row

st.set_page_config(page_title="🧪 Tasks CRUD", layout="wide")
st.title("🧪 Tasks – Simple CRUD Demo")

conn = get_connection()

# ----------------------------
# Add new task
# ----------------------------
st.subheader("Add new task")

with st.form("add_task_form"):
    new_title = st.text_input("Title")
    new_priority = st.selectbox("Priority", ["low", "medium", "high"])
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if not new_title.strip():
            st.warning("Title required")
        else:
            insert_row(
                conn,
                "tasks",
                {"title": new_title, "priority": new_priority, "done": 0},
            )
            st.success(f"Task '{new_title}' added")

# ----------------------------
# Display and edit tasks
# ----------------------------
st.subheader("Tasks")

df = fetch_rows(conn, "tasks")

if df.empty:
    st.info("No tasks yet")
else:
    # Make ID read-only
    column_config = {
        "id": st.column_config.NumberColumn("ID", disabled=True)
    }

    edited_df = st.data_editor(
        df,
        column_config=column_config,
        num_rows="dynamic",
        use_container_width=True,
    )

    # ----------------------------
    # Update changes
    # ----------------------------
    if st.button("Save changes"):
        updated_count = 0
        for _, row in edited_df.iterrows():
            original = df.loc[df["id"] == row["id"]].iloc[0]
            changes = {col: row[col] for col in df.columns if row[col] != original[col]}
            if changes:
                update_row(conn, "tasks", int(row["id"]), changes)
                updated_count += 1
        st.success(f"{updated_count} task(s) updated")

    # ----------------------------
    # Delete selected task
    # ----------------------------
    st.subheader("Delete task")
    task_to_delete = st.selectbox("Select Task ID to delete", df["id"].tolist())
    if st.button("Delete Task"):
        delete_row(conn, "tasks", task_to_delete)
        st.warning(f"Task {task_to_delete} deleted")

conn.close()
