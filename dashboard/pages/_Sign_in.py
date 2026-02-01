"""
Authentication page (Login & Registration)

This page handles:
- Doctor login 
- Doctor registration
- Session control using Streamlit session_state
"""

import streamlit as st 
import json 
from pathlib import Path

# ====== PAGE CONFIG ======
st.set_page_config(
    page_title= "ECG Analysis Dashboard | Sign In & Sign Up",
    page_icon= "🫀",
    layout= "centered"
)

# ====== SESSION INIT ======

USERS_PATH = Path("data/auth/users.json")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False 

if "user" not in st.session_state:
    st.session_state.user = None

# ====== HELPERS ======

def load_users():
    if not USERS_PATH.exists():
        return{}
    with open(USERS_PATH,"r") as f:
        return json.load(f)

def save_users(users: dict):
    USERS_PATH.parent.mkdir(parents= True, exist_ok= True)
    with open(USERS_PATH, "w") as f:
        json.dump(users, f, indent= 4)

def login_user(cpf: str, password: str) -> bool:
    users = load_users()
    return cpf in users and users[cpf]["password"] == password

def register_user(form_data: dict):
    """
    Temporary registration logic. 
    Future: save to database. 
    """
    st.success("Registration successful!")
    st.info("You can now log in.")

# ====== UI ======
st.title("🫀 ECG Analysis Dashboard")
st.subheader("Doctor's access")

# ====== TAB MANAGER ======
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "login"

if "register_success" not in st.session_state:
    st.session_state.register_success = False

tab_index = 0 if st.session_state.active_tab == "login" else 1

if st.session_state.get("register_success", False):
    st.success("Registration successful! You can now log in using your CPF and password.")
    st.session_state.register_success = False

tab_login, tab_register = st.tabs(
    ["🔐 Sign In", "📝 Sign Up"]
)

# ====== LOGIN TAB ======
with tab_login:
    st.markdown("### Enter the system")
    
    if st.session_state.register_success:
        st.success("Registration successful! you can log in now.")
        st.session_state.register_success = False

    cpf = st.text_input("CPF", placeholder= "Only numbers")
    password = st.text_input("Password", type="password")

    if st.button("Enter"):
        if login_user(cpf, password):
            st.session_state.authenticated = True 
            st.session_state.user = {"cpf":cpf}
            st.success("Login successful!")
            st.switch_page("pages/_Home.py")
        else:
            st.error("Invalid CPF or password")

# ====== REGISTER TAB ======
with tab_register:
    st.markdown("### Registration of the doctor")

    with st.form("register_form"):
        st.markdown("### Personal data")
        name = st.text_input("Full name")
        cpf_reg = st.text_input("CPF")
        rg = st.text_input("RG")
        birth_date = st.date_input("Date of birth")
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])

        st.markdown("### Contact")
        phone = st.text_input("Telephone")
        email = st.text_input("E-mail")

        st.markdown("### Professional data")
        crm = st.text_input("CRM - Number")
        crm_state = st.selectbox("CRM - Regional State", ["CRM-PB","CRM-MG","CRM-AM","CRM-SP", "CRM-RJ"])
        speciality = st.text_input("Main specialty")
        subspecialty = st.text_input("Subspecialties (optional)")

        st.markdown("### Security")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm password", type="password") 

        submitted = st.form_submit_button("Sign Up")

        if submitted:
            # confirm password verification
            if password != password_confirm: 
                st.error("Passowords do not match")
                st.stop()
            
            users = load_users()

            # already cpf registered verification
            if cpf_reg in users:
                st.error("CPF already registered")
                st.stop()
            
            users[cpf_reg] = {
                "name": name, 
                "password": password,
                "crm": crm,
                "crm_state": crm_state,
                "speciality": speciality
            }

            save_users(users)

            st.session_state.register_success = True
            st.rerun()