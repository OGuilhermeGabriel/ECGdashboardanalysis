#file for io's - read de input file and return the output files

import numpy as np 
from scipy.io import loadmat

def load_ecg_signal(mat_path, signal_key, fs):
    """
    Loading the ECG signal from a .mat files

    --- Parameters ---

    mat_path : str
        Pathing to the .mat input file
    signal_key : str
        Name of the variable inside of the .mat file (ex: 'test')
    fs : float 
        Sampling Frequency (Hz)
    
    --- Returns ---
    dict 
        Dictionary contains:
        - signal : np.ndarray
        - fs : float 
        - time : np.ndarry 
        - n_samples : int
    """

    #loading the .mat input file 
    mat_data = loadmat(mat_path)

    if signal_key not in mat_data:
        raise KeyError(f"Variable '{signal_key}' not finded in this .mat file")

    #extracting the signal and guaranteeing the 1d format
    x = mat_data[signal_key].squeeze()

    #number of the total of n_samples
    n_samples = len(x)

    #time vector
    t = np.arange(n_samples)/fs 

    return{
        "signal": x,
        "fs": fs,
        "time": t,
        "n_samples": n_samples
    }
