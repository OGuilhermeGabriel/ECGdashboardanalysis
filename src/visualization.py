#file for visualization - plotting graphics 

"""
visualization.py is responsible for the visualization of the raw and filtered signal, besides to visualize the media of the energy and the thresholds

This file receives all the data and converts to the graphics to the dashboard
"""

import numpy as np 
import matplotlib.pyplot as plt 

# ====== AUXILIARY FUNCTION ======
def _base_time_plot(ax):
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Amplitude")
    ax.grid(True)

# ====== PLOTTING FUNCTIONS: TIME DOMAIN ======
def plot_ecg_raw(time, signal):
    """
    Plot raw ECG signal in time domain
    """
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(time, signal, label="Raw ECG")
    ax.set_title("ECG Signal (Raw)")
    _base_time_plot(ax)
    ax.legend()

    return fig

def plot_ecg_filtered(time, signal_filt):
    """
    Plot filtered ECG signal in time domain
    """
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(time, signal_filt, label="Filtered ECG", color="orange")
    ax.set_title("ECG Signal (Filtered)")
    _base_time_plot(ax)
    ax.legend()
    
    return fig

def plot_ecg_comparison(time, signal, signal_filt):
    """
    Plot raw vs filtered ECG signal in time domain
    """
    fig, ax = plt.subplots(figsize= (12,4))
    ax.plot(time, signal, label="Raw ECG", alpha=0.6)
    ax.plot(time, signal_filt, label="Filtered ECG", linewidth=1.5)
    ax.set_title("ECG Signal: Raw vs Filtered")
    _base_time_plot(ax)
    plt.legend()

    return fig

# ====== PLOTTING FUNCTIONS: FREQUENCY DOMAIN ======

def plot_spectrum_raw(freq, magnitude):
    """
    Plot frequency spectrum of raw ECG signal
    """
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(freq, magnitude)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Frequency Spectrum (Raw ECG)")
    ax.grid(True)

    return fig

def plot_spectrum_filtered(freq, magnitude):
    """
    Plot frequency spectrum of filtered ECG signal
    """
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(freq, magnitude, color="orange")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Frequency Spectrum (Filtered ECG)")
    ax.grid(True)

    return fig

def plot_spectrum_comparison(freq, mag_raw, mag_filt):
    """
    Plot frequency spectrum comparison (raw vs filtered)
    """
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(freq, mag_raw, label="Raw ECG", alpha=0.6)
    ax.plot(freq, mag_filt, label="Filtered ECG", linewidth=1.5)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Frequency Spectrum: Raw vs Filtered")
    ax.legend()
    ax.grid(True)

    return fig 

def plot_energy(time_windows, energy):
    """
    Plot windowed energy over time
    """
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(time_windows, energy, label= "Windowed Energy")
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Energy")
    ax.set_title("Windowed Energy")

    return fig

def plot_energy_with_thresholds(time, delta_energy, mean_delta, threshold_pos, threshold_neg, events=None):
    """
    Plot energy with statistical thresholds and detected events. 

    Parameters
    ----------
    time: np.ndarray 
        Time vector associated with delta_energy
    delta_energy: np.ndarray 
        Energy variation between consecutive windows 
    mean_delta: float 
        Mean of delta_energy 
    threshold_pos: float 
        Upper detection threshold 
    threshold_neg: float 
        Lower detection threshold
    events: np.ndarray (bool)
        Boolean array indicating detected anomalou events
    """

    fig, ax = plt.subplots(figsize=(12,4))

    #delta energy plotting 
    ax.plot(time, delta_energy, label= "Δ Energy", color= "red")

    #statistics
    ax.axhline(mean_delta, linestyle="--", color="green", label="Mean ΔE")
    ax.axhline(threshold_pos, linestyle="--", color="blue", label="Upper threshold")
    ax.axhline(threshold_neg, linestyle="--", color="blue", label="Lower threshold")

    #detected events conditional 
    if events is not None:
        ax.scatter(
            time[events],
            delta_energy[events],
            color="yellow",
            edgecolors="black",
            label= "Detected events",
            zorder= 5
        )
    
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Δ Energy")
    ax.set_title("Energy Variation with Anomaly Detection")
    ax.legend()
    ax.grid(True)

    fig.tight_layout()
    return fig