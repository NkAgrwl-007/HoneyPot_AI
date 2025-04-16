import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth import authenticate_user  # Import authenticate_user function

st.set_page_config(page_title="Login - Honeypot-AI", page_icon="🔐")

# Redirect if already logged in
if st.session_state.get("logged_in"):
    st.success(f"✅ Welcome back, {st.session_state.get('username')}!")
    st.switch_page("dashboard")  # Navigate to dashboard page

st.title("🔐 Login - Honeypot-AI")

# Input fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

st.markdown("")

# Login button logic
if st.button("Login"):
    if authenticate_user(username, password):  # Check if credentials are valid
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success("✅ Login successful! Redirecting to dashboard...")
        st.switch_page("Dashboard")  # Navigate to dashboard page
    else:
        st.error("❌ Invalid credentials")

# Button to navigate to signup page
if st.button("Create Account"):
    st.session_state["page"] = "signup"
    st.switch_page("Signup")  # Switch to the sign-up page
