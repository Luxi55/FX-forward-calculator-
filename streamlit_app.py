import streamlit as st

st.set_page_config(page_title="FX-Forward Calculator", layout="centered")
st.sidebar.title("Navigation")
st.sidebar.page_link("pages/01_home.py", label="Home")
st.sidebar.page_link("pages/02_input.py", label="Input")
st.sidebar.page_link("pages/03_result.py", label="Result")