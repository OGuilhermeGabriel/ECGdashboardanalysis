#file for frequency spectral analysis
"""
spectral.py file is responsible for extracting spectral information from the signal

In this file, we're going to:
    - Compute the FFT from the input signal to return the frequencies, spectrum modulus and phase 
    - Get the power spectral density (PSD)
    - Do the spectral band extraction in some bands like 0.5 ~ 5 Hz
"""

import numpy as np 
from scipy.signal import welch 

def compute_fft(signal, fs):
    """
    Compute FFT of a 1D input signal

    Parameters 
    ----------
    signal: np.ndarray
        Input signal 
    fs: float 
        Sampling frequency (Hz)

    Returns 
    -------
    dict containing:
        - freq: frequency vector (Hz)
        - magnitude: magnitude spectrum 
        - phase: phase spectrum (rad)
    """

    n = len(signal)

    # FFT
    X = np.fft.fft(signal)
    freq = np.fft.fftfreq(n, d=1/fs)

    # Catching only the positive part of the spectrum 
    pos_mask = freq >= 0

    return {
        "freq":freq[pos_mask],
        "magnitude": np.abs(X[pos_mask]),
        "phase": np.angle(X[pos_mask])
    }

def compute_psd(signal, fs, nperseg=1024):
    """
    Compute power spectral density using welch method
    
    Parameters 
    ----------
    signal : np.ndarray 
        Inputl singal 
    fs : float 
        Sampling frequency (Hz)
    nperseg : int 
        Segment length for Welch 

    Returns 
    -------
    dict containing: 
        - freq : frequency vector (Hz)
        - psd : power spectral density 
    """

    freq, psd = welch(signal, fs=fs, nperseg=nperseg)

    return {
        "freq": freq, 
        "psd": psd
    }