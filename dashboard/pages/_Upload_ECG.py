import streamlit as st
import os, uuid, json
from datetime import datetime
from auth import require_auth

# ====== AUTH GUARD ======
require_auth()

# ====== PAGE CONFIG ======
st.set_page_config(
    page_title= "ECG Analysis Dashboard | Upload",
    page_icon= "➕",
    layout= "wide"
)
# ====== PATHS ======
BASE_DATA_PATH= "data/processed"
ECG_PATH= os.path.join(BASE_DATA_PATH, "ecg_files")
META_PATH= os.path.join(BASE_DATA_PATH, "metadata")

os.makedirs(ECG_PATH, exist_ok= True)
os.makedirs(META_PATH, exist_ok= True)

# ====== TITLE ======
st.title("ECG exam registration")
st.markdown("### 📤 Upload the ECG signal (.mat)")

# ====== ECG FILE UPLOAD ======
uploaded_file = st.file_uploader(
    "Select the ECG file",
    type=["mat"]
)
st.divider()

# ====== PATIENT FORM ======
st.markdown("### 🧍 Patient Form")

with st.form("patient_form"):
    patient_name = st.text_input("Full Name")
    patient_age = st.number_input(
        "Age",
        min_value= 1,
        max_value = 120,
        step= 1
    )
    patient_sex = st. selectbox("Sex", ["Male", "Female", "Other"])

    st.markdown("### 🩺 Exam Information")

    exam_condition = st.selectbox(
        "Exam conditions",
        [
            "Routine",
            "Pre-operative",
            "Symptom investigation"
        ]
    )

    exam_history = st.text_area(
        "Relevant medical history",
        placeholder= "Previous heart attack, cardiac surgeries, etc."
    )

    submitted = st.form_submit_button("💾 Save ECG and Patient Data")
    
# ====== HANDLE SUBMISSION ======
if submitted:
    if not uploaded_file:
        st.error("❌ No ECG file was uploaded.")
    elif patient_name.strip() == "":
        st.error("❌ The patient's name is required.")
    else: 
        exam_id = str(uuid.uuid4())

        ecg_filename = f"{exam_id}.mat"
        meta_filename = f"{exam_id}.json"

        #saving the ecg file
        with open(os.path.join(ECG_PATH, ecg_filename), "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        #building metadata
        metadata = {
            "exam_id": exam_id, 
            "created_at": datetime.now().isoformat(),
            "medic": st.session_state.get("medic_name", "Unknown"),
            "patient":{
                "name": patient_name,
                "age": patient_age,
                "sex": patient_sex
            },
            "exam_info":{
                "condition": exam_condition, 
                "history": exam_history, 
            }, 
            "ecg_file": ecg_filename
        }

        # Save matedata 
        with open(os.path.join(META_PATH, meta_filename), "w") as f:
            json.dump(metadata, f, indent= 4)

        st.success("✅ ECG exam successfully registered!")
        st.info("You can now view and analyze this exam in the corresponding tab.") 
