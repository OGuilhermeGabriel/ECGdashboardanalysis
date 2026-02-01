#file for energy analysis

"""
energy.py is the file responsible for calculate the signal energy over time, using in this case sliding windows

By calculating the energies of each sliding window, we obtain a way to detect peaks and anomalous events, get the segmented heartbeats and have a basis for the thresholding
"""

import numpy as np 

#sanity check
def signal_energy(signal):
    return np.sum(signal**2)

def windowed_energy(signal, window_size, hop_size):
    """
    Compute short-time energy of a signal based on the window size
    
    Parameters
    ----------
    signal: np.ndarray 
    window_size: int 
        Window length in samples 
    hop_size: int 
        Hop size in samples 

    Returns 
    -------
    energy: np.ndarry
        Energy per window
    """

    n = len(signal)
    energy = []

    for start in range(0, n-window_size + 1, hop_size):
        window = signal[start:start+window_size]
        e = np.sum(window ** 2)/window_size
        energy.append(e)
    
    return np.array(energy)