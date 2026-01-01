# engine/admin_panel.py
"""
Generic admin panel for PalantirLite tables.

- Reads models.yaml
- Shows editable tables
- Safely updates only changed cells
- YAML-driven for schema awareness
"""

import streamlit as st
import pandas as pd
from engine.db import get_connection
from engine.model_loader import load_models
from engine.crud import fetch_rows, update_row, insert_row

st.set_page_config(page_title="PalantirLite Admin Panel", layout="wide")
st.title("🧪 PalantirLite Admin Panel")

# ----------------------------
# Load schema
# ----------------------------
models = load_models()
conn = get_connection()

for table_name, table_def in models.items():
    st.header(f"Table: {table_name}")

    fields = table_def["fields"]

    # Fetch current data
    df = fetch_rows(conn, table_name)

    if df.empty:
        st.info(f"No rows in table '{table_name}' yet")
        continue

    # Determine which columns are read-only (pk)
    column_config = {}
    for col_name, cfg in fields.items():
        if cfg.get("pk", False):
            column_config[col_name] = st.column_config.NumberColumn(col_name, disabled=True)

    # Editable DataFrame
    edited_df = st.data_editor(
        df,
        column_config=column_config,
        num_rows="dynamic",
        use_container_width=True,
    )

    # Save changes
    if st.button(f"Save changes to {table_name}"):
        updated_count = 0
        for _, row in edited_df.iterrows():
            original = df.loc[df[fields.keys()] == row[fields.keys()]].iloc[0] if not df.empty else pd.Series()
            # Collect only changed cells
            changes = {col: row[col] for col in df.columns if row[col] != original.get(col, None)}
            if changes:
                pk_cols = [col for col, cfg in fields.items() if cfg.get("pk")]
                if not pk_cols:
                    st.error(f"No primary key defined for {table_name}, cannot update row")
                    continue
                pk_val = {col: row[col] for col in pk_cols}
                # For simplicity, assume single PK
                update_row(conn, table_name, int(list(pk_val.values())[0]), changes)
                updated_count += 1
        st.success(f"{updated_count} row(s) updated in {table_name}")

conn.close()
