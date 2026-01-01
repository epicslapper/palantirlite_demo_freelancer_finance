import streamlit as st
from engine.db import get_connection
from engine.crud import fetch_rows, insert_row, update_row

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

df = fetch_rows(conn, "tasks")

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
