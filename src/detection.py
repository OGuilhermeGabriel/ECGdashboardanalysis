#file for detection analysis

"""
detection.py is the file responsible for detecting anomalous events
based on energy variation statistics. 
"""

import numpy as np 

def detect_energy_anomalies(
        energy,
        time,
        std_factor= 1.5,
        use_absolute_delta= False
):
    """
    Parameters 
    ----------
    energy: np.ndarray
        Energy values per window or per heartbeat
    time: np.ndarray
        Time vector aligned with energy 
    std_factor: float 
        Multiplier for standard deviation (threshold sensitivity)
    use_absolute_data: bool 
        If True, uses |ΔE| instead of signed ΔE

    Returns 
    -------
    dict 
        Dictionary containing:
        - delta_energy
        - mean_delta
        - std_delta
        - threshold_pos
        - threshold_neg
        - events (boolean array)
        - event_times
    """

    # energy variation
    delta_energy = np.diff(energy)
    # temporal alignment
    time_valid = time[1:]
    #using modulus, to detect abrupt variations
    if use_absolute_delta:
        delta_used = np.abs(delta_energy)
    else:
        delta_used = delta_energy
    
    #defining the statistical reference
    mean_delta = np.mean(delta_used)
    std_delta = np.std(delta_used)
    
    #defining the thresholds
    threshold_pos = mean_delta + std_factor * std_delta
    threshold_neg = mean_delta - std_factor * std_delta

    #defining the decision rule for detection - events it's a boolean vector
    events = (delta_used > threshold_pos)|(delta_used < threshold_neg)

    # extracting the interesting times for analysis from the vector "events"
    event_times = time_valid[events]

    return {
        "delta_energy": delta_energy,
        "mean_delta": mean_delta,
        "std_delta": std_delta,
        "threshold_pos": threshold_pos,
        "threshold_neg": threshold_neg,
        "events": events,
        "event_times": event_times,
        "time": time_valid
    }