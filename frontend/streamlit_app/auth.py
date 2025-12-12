import streamlit as st
from db import add_user, validate_user, create_user_table, reset_password
from streamlit.runtime.scriptrunner import RerunException, get_script_run_ctx

create_user_table()

def login_page():
    st.markdown("### 🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = validate_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success(f"✅ Welcome {user[1]}!")
            raise RerunException(get_script_run_ctx())
        else:
            st.error("❌ Invalid email or password.")

def signup_page():
    st.markdown("### 📝 Create Account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        if add_user(username, email, password):
            st.info("ℹ️ Now login using your credentials.")
            raise RerunException(get_script_run_ctx())

def reset_password_page():
    st.markdown("### 🔄 Reset Password")
    email = st.text_input("Email for reset")
    new_password = st.text_input("New Password", type="password")
    if st.button("Reset Password"):
        if reset_password(email, new_password):
            st.info("ℹ️ Now login using your new password.")
            raise RerunException(get_script_run_ctx())

def auth_router():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    page = st.sidebar.selectbox("Authentication", ["Login", "Signup", "Reset Password"])

    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as {st.session_state.user[1]}")
        return True

    if page == "Login":
        login_page()
    elif page == "Signup":
        signup_page()
    else:
        reset_password_page()

    return False
