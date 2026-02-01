# ====== LIBRARIES ======
import matplotlib.pyplot as plt
import numpy as np

# ====== IMPORTS ======
from src.io_utils import load_ecg_signal
from src.preprocessing import bandpass_fir_filter
from src.config import FS, FILTER_CONFIG, ANOMALY_DETECTION_CONFIG
from src.spectral import compute_fft, compute_psd
from src.energy import windowed_energy
from src.visualization import plot_ecg_raw, plot_ecg_filtered, plot_ecg_comparison, plot_spectrum_raw, plot_spectrum_filtered, plot_spectrum_comparison, plot_energy_with_thresholds
from src.detection import detect_energy_anomalies

# ====== LOAD ECG SIGNAL ======
data = load_ecg_signal(
    mat_path="data/raw/Sinal.mat",
    signal_key="teste",
    fs=FS
)

x = data["signal"]
fs = data["fs"]
t = data["time"]

print("Signal loaded successfully")
print(f"Samples: {len(x)} | Fs: {fs} Hz")

# ====== PREPROCESSING: BANDPASS FILTER ======
x_filt = bandpass_fir_filter(
    signal=x,
    fs=fs,
    order=FILTER_CONFIG["order"],
    fc_low=FILTER_CONFIG["fc_low"],
    fc_high=FILTER_CONFIG["fc_high"],
    window=FILTER_CONFIG["window"]
)

print("Filtering completed successfully")

# ====== SPECTRAL: COMPUTING FFT, PSD  ======
fft_raw= compute_fft(x, fs)
fft_filt= compute_fft(x_filt, fs)
print(f'FFT computed')

psd_raw= compute_psd(x, fs)
psd_filt= compute_psd(x_filt, fs)
print(f'PSD computed')

# ====== ENERGY: COMPUTING ENERGY PER WINDOW ======
window_size = int(0.2 * fs)   #200 ms
hop_size = int(0.05 * fs)     #50 ms

energy_sig = windowed_energy(x_filt, window_size, hop_size)
time_energy = np.arange(len(energy_sig))*(hop_size/fs)

print("Energy computed")
print("Energy shape:", energy_sig.shape)
print("Energy max:", energy_sig.max())

# ====== DETECTION: DETECTING ANOMALIES ======
detection_result = detect_energy_anomalies(
    energy= energy_sig,
    time= time_energy,
    std_factor=ANOMALY_DETECTION_CONFIG["std_factor"],
    use_absolute_delta=ANOMALY_DETECTION_CONFIG["use_absolute_delta"]
)

n_events = np.sum(detection_result["events"])
print(f"Total events detected: {n_events}")

# ====== VISUALIZATION: PLOTTING GRAPHICS ======
figures = [
    plot_ecg_raw(t, x),
    plot_ecg_filtered(t, x_filt),
    plot_ecg_comparison(t, x, x_filt),
    plot_spectrum_raw(fft_raw["freq"], fft_raw["magnitude"]),
    plot_spectrum_filtered(fft_filt["freq"], fft_filt["magnitude"]),
    plot_spectrum_comparison(
        fft_raw["freq"],
        fft_raw["magnitude"],
        fft_filt["magnitude"]
    ),
    plot_energy_with_thresholds(
        detection_result["time"],
        detection_result["delta_energy"],
        detection_result["mean_delta"],
        detection_result["threshold_pos"],
        detection_result["threshold_neg"],
        detection_result["events"]
    )
]

plt.show()
plt.close("all")

# ====== BASIC SANITY CHECKS ======
print("NaNs in filtered signal:", np.isnan(x_filt).any())
print("Signal energy (raw):", np.sum(x**2))
print("Signal energy (filtered):", np.sum(x_filt**2))