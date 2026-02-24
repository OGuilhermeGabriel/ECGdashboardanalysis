"""
config.py

ECG analysis experiment configuration file.
Defines ALL pipeline hyperparameters.
It not contains processing logic.
"""

# --- Signal parameters --- 
# Expected sampling frequency of the ECG signal (Hz)
FS = 360 
#time unit 
TIME_UNIT = "seconds"

# --- Band-pass filter (FIR) parameters ---
FILTER_CONFIG = {
    "type"      : "FIR",
    "design"    : "window",
    "window"    : "hanning",
    "order"     : 10,
    "fc_low"    : 0.5,
    "fc_high"   : 4.0
}

# --- Spectral analysis parameters ---
SPECTRAL_CONFIG = {
    "fft_size"          : 1024,
    "window"            : "hamming",
    "max_windows_dft"   : 10
}

# --- R peak detection parameters ---
R_PEAK_CONFIG = {
    "min_peak_height"       : 0.5, #minimum height
    "min_peak_distance_sec" : 0.4 #minimum fisiologic distance (seconds)
}

# --- Energy parameters ---
ENERGY_CONFIG = {
    "window_type"       : "hanning",
    "energy_definition" : "sum_of_squares"
}

# --- Detecting anomalies (arrhythmais) parameters ---
ANOMALY_DETECTION_CONFIG ={
    "method"            : "energy_variation",
    "std_factor"        : 1.5, #multiplier for the standard deviation
    "use_absolute_delta": False
}

# --- Visualization parameters --- 
PLOT_CONFIG = {
    "show_grid"     : True, 
    "default_color" : "blue",
    "event_color"   : "yellow"
}
