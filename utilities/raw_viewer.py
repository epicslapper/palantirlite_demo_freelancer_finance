import streamlit as st
import pandas as pd

st.title("Raw Client Data Viewer")

#  TODO for chatgpt : sstart in the project dir



uploaded = st.file_uploader("Upload Excel or CSV", type=["csv", "xlsx"])

if uploaded:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.dataframe(df, width="stretch")
