#Visualization and analysis of the ecg signal
# ====== LIBRARIES IMPORTS ======
import sys
import streamlit as st
import os, json
import numpy as np 
import scipy.io as sio 
from pathlib import Path 
from auth import require_auth

# Adding project root to PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

# ====== PIPELINE IMPORTS ======
from src.config import FS, FILTER_CONFIG, ANOMALY_DETECTION_CONFIG
from src.preprocessing import bandpass_fir_filter
from src.spectral import compute_fft
from src.energy import windowed_energy
from src.detection import detect_energy_anomalies
from src.visualization import(
    plot_ecg_raw,
    plot_ecg_filtered,
    plot_ecg_comparison,
    plot_spectrum_raw,
    plot_spectrum_filtered,
    plot_spectrum_comparison,
    plot_energy_with_thresholds
)

# ====== AUTH GUARD ======
require_auth()

# ====== PAGE CONFIG ======
st.set_page_config(
    page_title= "ECG Analysis Dashboard | Analysis",
    page_icon= "📊",
    layout= "wide"
)

# ====== PATHS ======
BASE_DATA_PATH = "data/processed"
ECG_PATH = os.path.join(BASE_DATA_PATH, "ecg_files")
META_PATH = os.path.join(BASE_DATA_PATH, "metadata")

# ====== TITLE ======
st.title("📊 ECG Signal Analysis")

# ====== SIDEBAR - INTERACTIVE PARAMETERS ======
st.sidebar.header("🎛️ Filter Parameters")

fc_low = st.sidebar.slider(
    "Low cutoff frequency (Hz)",
    min_value= 0.1,
    max_value= 40.0, 
    value= FILTER_CONFIG["fc_low"],
    step= 0.1
)

fc_high = st.sidebar.slider(
    "High cutoff frequency (Hz)",
    min_value= 10.0,
    max_value= 100.0,
    value= FILTER_CONFIG["fc_high"],
    step= 1.0
)

if fc_low >= fc_high:
    st.sidebar.error("Low cutoff must be smaller than high cutoff")
    st.stop()

st.sidebar.header("⚡ Anomaly Detection")

std_factor = st.sidebar.slider(
    "Detection sensitivity (σ)",
    min_value= 2.0,
    max_value= 5.0,
    value= ANOMALY_DETECTION_CONFIG["std_factor"],
    step= 0.1
)

# ====== LOAD METADATA ======
metadata_files = [
    f for f in os.listdir(META_PATH) if f.endswith(".json")
]

if not metadata_files:
    st.warning("No ECG exams registered yet")
    st.stop()

# ====== SELECT EXAM ======
exam_labels = {}

for file in metadata_files:
    with open(os.path.join(META_PATH, file)) as f:
        meta = json.load(f)
    label = (
        f"{meta['patient']['name']} | "
        f"{meta['patient']['age']}y | "
        f"{meta['exam_info']['condition']} | "
        f"{meta['created_at'][:10]}"
    )
    exam_labels[label] = file

selected_label = st.selectbox(
    "Select an ECG exam",
    list(exam_labels.keys())
)
selected_meta = exam_labels[selected_label]

# ====== LOAD METADATA ======
with open(os.path.join(META_PATH, selected_meta)) as f:
    metadata = json.load(f)

st.markdown("### 🧍 Patient Information")
col1, col2, col3 = st.columns(3)

with col1: 
    st.metric("👤 Name", metadata["patient"]["name"])

with col2:
    st.metric("🎂 Age", f"{metadata['patient']['age']} years")

with col3:
    st.metric("⚧ Sex", metadata["patient"]["sex"])

st.markdown("### 🩺 Exam Information")

st.markdown(f"""
- **Condition:** {metadata["exam_info"]["condition"]}
- **Clinical history:** {metadata["exam_info"]["history"] or "Not informed"}
""")
# ====== LOAD ECG SIGNAL ======
ecg_file = metadata["ecg_file"]
mat_data = sio.loadmat(os.path.join(ECG_PATH, ecg_file))

#if the name of de .mat signal file it's different, adjust it
signal_key = list(mat_data.keys())[-1]
x = mat_data[signal_key].squeeze()

fs = FS
t = np.arange(len(x))/fs

# ====== CACHED PROCESSING ======
@st.cache_data(show_spinner= False)
def compute_filtered_signal(x, fs, fc_low, fc_high):
    return bandpass_fir_filter(
        signal= x,
        fs= FS,
        order= FILTER_CONFIG["order"],
        fc_low= fc_low, 
        fc_high= fc_high, 
        window= FILTER_CONFIG["window"]
    )

@st.cache_data(show_spinner= False)
def compute_energy_and_detection(x_filt, fs, std_factor):
    window_size = int(0.2 * fs)
    hop_size = int(0.05 * fs)

    energy = windowed_energy(x_filt, window_size, hop_size)
    time_energy = np.arange(len(energy)) * (hop_size/fs)

    detection = detect_energy_anomalies(
        energy= energy,
        time= time_energy, 
        std_factor= std_factor,
        use_absolute_delta= ANOMALY_DETECTION_CONFIG["use_absolute_delta"]
    )

    return energy, time_energy, detection

# ====== PIPELINE ======
x_filt = compute_filtered_signal(x, fs, fc_low, fc_high)

fft_raw = compute_fft(x, fs)
fft_filt = compute_fft(x_filt,fs)

energy, time_energy, detection = compute_energy_and_detection(x_filt, fs, std_factor)

# ====== VISUALIZATION ======
st.markdown("## ⏱ Time Domain")
st.pyplot(plot_ecg_comparison(t, x, x_filt))

st.markdown("## 📈 Frequency Domain")
st.pyplot(
    plot_spectrum_comparison(
        fft_raw["freq"],
        fft_raw["magnitude"],
        fft_filt["magnitude"]
    )
)

st.markdown("## ⚡ Energy & Anomaly Detection")
st.pyplot(
    plot_energy_with_thresholds(
        detection["time"],
        detection["delta_energy"],
        detection["mean_delta"],
        detection["threshold_pos"],
        detection["threshold_neg"],
        detection["events"],
    )
)

st.success(f"DETECTED EVENTS: {int(np.sum(detection['events']))}")