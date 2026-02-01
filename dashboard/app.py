#file for main application config
import streamlit as st 

# ====== PAGE CONFIGURATION ======
st.set_page_config(
    page_title="ECG Analysis Dashboard",
    page_icon= "❤️",
    layout= "wide",
    initial_sidebar_state= "expanded",
)

# ====== SESSION STATE INT ======
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = None 

# ====== ACCESS CONTROL ======
def require_login():
    """
    Blocks acess to pages if the user is not logged in
    """
    if not st.session_state.logged_in:
        st.warning("⚠️ Please log in to access the system.")
        st.stop()

# ====== MAIN PAGE (LANDING PAGE) ======

st.title("🫀 ECG Analysis Dashboard")

# ====== NOT LOGGED IN ======

if not st.session_state.logged_in:
    st.info(
        """
        **Welcome to the ECG Analysis Dashboad.**
        
        Please log in or register to continue.
        """
    )
    st.markdown("👉 Use the sidebar to access the **Sign In** page.")
    st.divider()

    st.header("📊 About the Project")
    st.markdown(
        """
        This dashboard was developed for **digital electrocardiogram (ECG) signal analysis**,
        focusing on **digital signal processing**.

        The system applies:
        - Digital filtering for noise removal
        - Spectral and temporal analysis
        - Energy-based methods to highlight anomalous cardiac events

        The goal is to provide a **visual, intuitive and practical tool** that assists
        physicians in clinical ECG exam analysis.
        """
    )
    st.divider()

    st.header("👨‍💻 About Me & Motivation")
    st.markdown(
        """
        My name is **Guilherme Gabriel**, I am 23 years old and currently studying
        **Computer Engineering**.

        This project was inspired by my enthusiasm for the **Digital Signal Processing**
        course, where I studied the modeling of digital filters and their application
        to biomedical signals.

        After completing the academic project, I envisioned transforming it into
        an **interactive dashboard**, where a physician could upload ECG exams,
        visualize processed signals and obtain insights that may support
        clinical decision-making.       
        """
    )
    st.divider()

    st.header("🔗 Connect with Me")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            "💼 **LinkedIn**  \n"
            "[linkedin.com/in/guilherme-gabriel](https://www.linkedin.com/in/guilherme-gabriel-5369691a2/)"
        )

    with col2:
        st.markdown(
            "💻 **GitHub**  \n"
            "[github.com/OGuilhermeGabriel](https://github.com/OGuilhermeGabriel)"
        )

    with col3:
        st.markdown(
            "🎥 **Project Explanation (YouTube)**  \n"
            "[Watch the video](https://www.youtube.com/)"
        )

# ====== LOGGED IN ======
else:
    st.success(f"Welcome, **Dr. {st.session_state.user_name}👨‍⚕️**")
    st.markdown(
        """
        Use the sidebar to:
        - 📥 Upload ECG signals
        - 📈 Analyze ECG exams
        - 🧠 Review detected anomalous events       
        """
    )

    