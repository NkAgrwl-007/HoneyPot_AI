import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth import register_user  # Corrected import to register_user

st.set_page_config(page_title="Sign Up - Honeypot-AI", page_icon="📝")

# Account creation form
st.title("📝 Create Account - Honeypot-AI")

# Input fields for account creation
new_username = st.text_input("New Username", key="create_username")
new_password = st.text_input("New Password", type="password", key="create_password")
confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

# Create Account button logic
if st.button("Create Account"):
    if new_password != confirm_password:
        st.error("❌ Passwords do not match")  # Check if passwords match
    else:
        result = register_user(new_username, new_password)  # Register user with the correct function
        if result.startswith("✅"):  # Success message
            st.success(result)
            # After account creation, automatically navigate to the login page
            st.session_state["page"] = "login"
            st.switch_page("Login")  # Switch to the login page
        else:  # Error message
            st.error(result)

# Option to redirect to login page
if st.button("Back to Login"):
    st.switch_page("Login")