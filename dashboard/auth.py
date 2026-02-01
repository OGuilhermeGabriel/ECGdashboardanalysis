import streamlit as st

def require_auth():
    if not st.session_state.get("authenticated", False):
        st.session_state["auth_message"] = (
            "🔒 Please log in to access the dashboard."
        )
        st.switch_page("pages/_Sign_in.py")