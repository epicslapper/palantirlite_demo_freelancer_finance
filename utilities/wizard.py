# FILE: wizard.py
import streamlit as st
import sqlite3
import shutil
import pandas as pd
import yaml
from pathlib import Path

# ----------------------------
# Config
# ----------------------------
DB_FILE = Path("app.db")
MODEL_FILE = Path("models.yaml")
BACKUP_FILE = DB_FILE.with_suffix(".backup.db")

# ----------------------------
# Helper functions
# ----------------------------
def get_conn():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def backup_db():
    shutil.copy(DB_FILE, BACKUP_FILE)
    st.success(f"Backup created: {BACKUP_FILE}")

def load_models():
    with open(MODEL_FILE) as f:
        return yaml.safe_load(f)

def get_db_columns(table_name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cursor.fetchall()]
    conn.close()
    return cols

def compare_schema():
    models = load_models()
    schema_diff = {}
    for table_name, table in models.items():
        yaml_cols = list(table["fields"].keys())
        db_cols = get_db_columns(table_name)
        missing = [c for c in yaml_cols if c not in db_cols]
        extra = [c for c in db_cols if c not in yaml_cols]
        schema_diff[table_name] = {"missing": missing, "extra": extra}
    return schema_diff

def apply_add_columns():
    models = load_models()
    conn = get_conn()
    cursor = conn.cursor()
    for table_name, table in models.items():
        db_cols = get_db_columns(table_name)
        for field, cfg in table["fields"].items():
            if field not in db_cols:
                col_type = {"integer":"INTEGER","text":"TEXT","float":"REAL","boolean":"INTEGER","enum":"TEXT"}.get(cfg["type"], "TEXT")
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {field} {col_type}")
    conn.commit()
    conn.close()
    st.success("Missing columns added successfully!")

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("Migration Assistant")

st.info("This wizard helps you safely migrate your SQLite DB schema according to your YAML definitions.")

# Step 1: Backup
st.subheader("Step 1: Ensure Backup")
if not BACKUP_FILE.exists():
    st.warning("No backup found. Please create one!")
if st.button("Create Backup"):
    backup_db()

# Step 2: Show Schema Differences
st.subheader("Step 2: Compare Schema")
diff = compare_schema()
for table, changes in diff.items():
    st.markdown(f"**Table: {table}**")
    st.write("Missing columns (in YAML but not DB):", changes["missing"])
    st.write("Extra columns (in DB but not YAML):", changes["extra"])

# Step 3: Apply safe migration
st.subheader("Step 3: Apply Add-Only Migration")
st.info("This step only adds missing columns. No DROP or DELETE will happen.")
if st.button("Apply Add-Only Migration"):
    apply_add_columns()
    st.success("Migration applied. Re-check schema to confirm.")

# Step 4: Done
st.subheader("Step 4: Done")
st.info("Check your DB using your usual app or DB browser. Only missing columns have been added.")
