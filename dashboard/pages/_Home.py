#home page for the application
import streamlit as st
from auth import require_auth

# ====== AUTO GUARD ======
require_auth()

# ====== PAGE CONFIG ======
st.set_page_config(
    page_title= "ECG Analysis Dashboard | Home",
    page_icon= "❤️",
    layout= "wide"
)

# ====== SIDE BAR ======
with st.sidebar:
    st.title("ECG Dashboard")
    st.divider()

    #logged-in doctor (example)
    medic_name = st.session_state.get("medic_name", "Medic")
    st.write(f"👨‍⚕️ **{medic_name}**")
    st.divider()

    if st.button("➕ Register the ECG signal"):
        st.switch_page("pages/_Upload_ECG.py")

    if st.button("📊 View and analyze ECGs"):
        st.switch_page("pages/_Analysis_ECG.py")


# ====== MAIN CONTENT ======
st.title("Welcome to the ECG Analysis Dashboard")

st.markdown(
    """
    This system was developed for **advanced ECG signal analysis**, allowing:
    
    - Visualization of raw and filtered signals
    - Spectral analysis (FFT)
    - Statistical detection of anomalies
    - Organization of exams by patient

    Use the side menu to begin.
    """
)

st.info(
    "👉 Start by registering a new ECG signal or view existing exams."
)