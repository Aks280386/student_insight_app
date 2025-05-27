import streamlit as st
from app.services.session_manager import init_session
from app.db.database import validate_login

# Initialize session
init_session()

def login_screen():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        role = validate_login(username, password)
        if role:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.rerun()  # to refresh the page after login
        else:
            st.sidebar.error("Invalid username or password")

# Check session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Run login screen or show success
if not st.session_state["logged_in"]:
    login_screen()
    st.stop()
else:
    st.success(f"Logged in as {st.session_state['username']} ({st.session_state['role']})")
    st.info("Please click on preferred page from the sidebar to continue.")