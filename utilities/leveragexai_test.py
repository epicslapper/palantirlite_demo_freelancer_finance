import streamlit as st
import yaml
from pathlib import Path
import sqlite3
import pandas as pd

DB_FILE = "testdata.db"
YAML_FILE = "models.yaml"

# -----------------------------
# Utility functions
# -----------------------------
def save_yaml(models):
    with open(YAML_FILE, "w") as f:
        yaml.dump(models, f)

def get_conn():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def create_tables(models):
    conn = get_conn()
    for table_name, table in models.items():
        cols = []
        for field, cfg in table["fields"].items():
            col_type = {"text": "TEXT", "integer": "INTEGER", "float": "REAL", "boolean": "INTEGER", "enum": "TEXT"}.get(cfg["type"], "TEXT")
            col_def = f"{field} {col_type}"
            if cfg.get("pk"):
                col_def += " PRIMARY KEY"
            if cfg.get("required"):
                col_def += " NOT NULL"
            cols.append(col_def)
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols)});"
        conn.execute(sql)
    conn.commit()
    conn.close()

def generate_test_data(models, rows_per_table=3):
    conn = get_conn()
    for table_name, table in models.items():
        for i in range(1, rows_per_table+1):
            data = {}
            for field, cfg in table["fields"].items():
                if cfg.get("pk"):
                    data[field] = i
                elif cfg["type"] == "text":
                    data[field] = f"{table_name}_{field}_{i}"
                elif cfg["type"] == "integer":
                    data[field] = i
                elif cfg["type"] == "float":
                    data[field] = i*1.1
                elif cfg["type"] == "boolean":
                    data[field] = i % 2
                elif cfg["type"] == "enum":
                    data[field] = cfg["values"][0]
            cols = ", ".join(data.keys())
            placeholders = ", ".join("?" for _ in data)
            conn.execute(f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})", list(data.values()))
    conn.commit()
    conn.close()

# -----------------------------
# Streamlit GUI
# -----------------------------
st.title("LeverageXAI YAML + Test Data Generator (Prototype)")

tab_yaml, tab_test = st.tabs(["Define YAML", "Generate Test Data"])

with tab_yaml:
    st.subheader("Define Tables")
    st.info("For simplicity, this prototype supports 1 table only. Extend as needed.")

    table_name = st.text_input("Table name", "tasks")
    n_fields = st.number_input("Number of fields", min_value=1, max_value=10, value=3, step=1)

    models = {table_name: {"fields": {}}}

    for i in range(n_fields):
        field_name = st.text_input(f"Field {i+1} name", f"field{i+1}")
        field_type = st.selectbox(f"Field {i+1} type", ["text", "integer", "float", "boolean", "enum"], key=f"type_{i}")
        required = st.checkbox("Required?", value=False, key=f"req_{i}")
        pk = st.checkbox("Primary Key?", value=False, key=f"pk_{i}")
        enum_values = None
        if field_type == "enum":
            enum_values_str = st.text_input("Enum values (comma separated)", "low,medium,high", key=f"enum_{i}")
            enum_values = [v.strip() for v in enum_values_str.split(",")]
        models[table_name]["fields"][field_name] = {"type": field_type, "required": required, "pk": pk}
        if enum_values:
            models[table_name]["fields"][field_name]["values"] = enum_values

    if st.button("Save YAML"):
        save_yaml(models)
        st.success(f"YAML saved to {YAML_FILE}")
        st.code(yaml.dump(models))

with tab_test:
    st.subheader("Generate Test Data & Populate DB")
    st.info("This will create tables from YAML and insert descriptive test data.")

    if st.button("Generate Test Data"):
        with open(YAML_FILE) as f:
            models = yaml.safe_load(f)
        create_tables(models)
        generate_test_data(models)
        st.success(f"Database {DB_FILE} populated with test data.")

        conn = get_conn()
        table_name = list(models.keys())[0]
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        st.dataframe(df)
