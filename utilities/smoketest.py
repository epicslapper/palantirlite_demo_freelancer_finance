import streamlit as st

# Test imports
try:
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
    st.success("✅ All engine modules imported successfully!")
except Exception as e:
    st.error(f"❌ Import error: {e}")

# Test DB connection
try:
    conn = get_connection()
    st.success("✅ DB connection works!")
    conn.close()
except Exception as e:
    st.error(f"❌ DB connection failed: {e}")

# Test model loading
try:
    models = load_models("models.yaml")
    st.success(f"✅ Models loaded: {list(models.keys())}")
except Exception as e:
    st.error(f"❌ Failed to load models: {e}")
