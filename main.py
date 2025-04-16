import streamlit as st

st.set_page_config(page_title="Honeypot-AI", layout="wide")
st.title("🚀 Honeypot-AI Security Portal")

choice = st.selectbox("Choose an option", ["Login", "Signup"])

if choice == "Login":
    st.switch_page("pages/Login.py")  # ✅ points to pages/Login.py
else:
    st.switch_page("pages/Signup.py")
