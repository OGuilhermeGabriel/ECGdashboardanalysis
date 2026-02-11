# ECG Analysis Dashboard
---

## Summary 

>- [*Project's Stack*](#projects-stack)
>- [*Instructions*](#instructions)
>- [*How the Dashboard works*](#how-the-dashboard-works)
>- [*The Digital Processing of the ECG Signal*](#the-digital-processing-of-the-ecg-signal)
>- [*The Software Architecture*](#the-software-architecture)
---

### Project's Stack 

- **Matplotlib**: for plotting signal graphs.
- **Numpy**: for performing the computational calculations for signal processing.
- **Streamlit**: for building the dashboard.
- **Scipy**: for uploading and implementing bandpass filtering
---

### Instructions
1) Clone this repository
2) Download the application dependencies described in requirements.txt
3) If you only want to access the pipeline that exemplifies the electrocardiogram signal processing, run: 
```python3 test_pipeline.py```

4) To run the dashboard: 
```streamlit run ./dashboard/app.py```
---

### How the Dashboard works 

#### Accessing the Dashboard

Once you run the dashboard, you will be redirected to the application's home page, which will only be the entry point to the application.

Access the "Sign In" option in the sidebar on the left of the application to log in to the system. If you don't have a registered account, create a new one in "Sign up". If you want to go directly to the dashboard without registering, use the admin account:

> *CPF: 00000000000*
> *password: admin*

#### Using the Dashboard
Upon logging into the system, you will have 3 additional options unlocked:

- Home page

This page will serve only as a brief introduction and the "hub" page once you are logged in.

- Register the ECG signal

On this page, you will register an ECG signal on your dashboard. This project only considers .mat signals for digital processing. Therefore, carefully observe the signal you are importing into the dashboard.

Furthermore, this signal you are registering will be related to a patient and, consequently, you will also need to fill out a form containing their information.

- View and Analyze ECGs

This is the most important page of the application. Here you will select the ECG signal you want to analyze, and then the dashboard will show you a comparison of the raw signal with the signal filtered by a bandpass filter.

You can and should change the cutoff frequency parameters of the bandpass filter to attenuate all undesirable frequencies. Use the frequency spectrum of the raw ECG signal provided by the dashboard as a basis and compare it with the frequency spectrum obtained after implementing the filter.

Once you have adjusted the bandpass filter, the filtered signal will deliver the desired frequencies for the analysis of the diagnosis of possible cardiac anomalies.

For this project, the analysis was based on energy variation: If at any point in the ECG signal there is a sudden energy variation and it passes either the positive or negative threshold, this point will be counted as an anomalous event. It's worth mentioning that the "detection sensitivity" parameter indicates how tolerant these energy spikes need to be to be considered anomalous events or not.

---

### The Digital Processing of the ECG Signal 

This topic will focus on explaining the signal filtering steps as well as the statistical method chosen to find possible anomalous events.

#### ECG Signal Preprocessing Step

When we receive electrocardiogram signals, we can see that the signals received are generally noisy, containing undesirable frequency components related to everything from the device's electrical network to the patient's muscle contractions. The table below relates the main frequency ranges obtained from a raw ECG signal and their respective real events:

| Frequency Range | Interpretation |
|-----------------|----------------|
|0 - 0.5 hz       | Baseline drift, respiration |
|0.5 - 3 hz       | Heart rhythm (QRS, P, T) |
|3 - 15 hz        | Cardiac harmonics |
|above 30 - 40 hz | Muscle noise, electrical network |


Therefore, even before we begin analyzing the signal, it becomes necessary to construct a digital filter and apply it to attenuate the inconvenient frequency components and leave only the components of interest: those originating from the patient's heartbeats.

##### The Construction of the Digital Filter

In this sense, we must create a digital filter that, in addition to filtering the desired frequency range for ECG analysis, requires consideration of the filter order and the windowing technique to be adopted.

- The choice of FIR filter

IIR type filters are faster in terms of computational processing than FIR filters when compared with the same filter order and, consequently, require fewer calculations and less computational power. However, there is a possibility of delays associated with this speed, which would compromise the accuracy of the filtered ECG signal.

Therefore, the type of filter chosen for the application was the FIR type due to its constant phase, guaranteeing the stability of the filtered ECG signal. On the other hand, the order of the FIR filter to be applied will be higher to compensate for the lack of computational power when compared to the IIR filter.

- The choice of bandpass filter

Notice that the frequency range table gives us a range of 0.5 - 40 Hz where we can obtain the frequency components that represent the heart rate and its harmonics.

Consequently, the most recommended approach is to use a bandpass filter composed of a lower and upper cutoff frequency, which determine our desired range.

*You might even think that, in terms of practicality, it would be better to use a low-pass filter, where frequencies above 40 Hz would be attenuated. However, the frequency components below 0.5 Hz would pass through the filter and add inaccuracies to the filtered signal. This would compromise the statistical analysis of the signal for the detection of anomalous events in the future...*

- The Choice of Windowing Technique

Choosing the type of windowing technique to be used is essential to avoid problems with ripples in the passbands located between the windows, edge effects, and spectral leakage of frequencies.

The technique I chose was the Hanning window, because in addition to smoothing the edges, it has less ripple in the passband compared to other windowing techniques such as Hamming.

This ensures better accuracy in the filtered components and fewer problems related to spectral leakage of frequencies. This improves the efficiency of the energy-per-period analysis that will be performed in the future to discover anomalous events.

#### ECG Signal Analysis Step

##### Energy calculation
##### Energy differences
##### Detection of possible anomalies

--- 

### The Dashboard Architecture
---

### Licensed 

This project is licensed under the ***MIT*** License. You are free to use, copy, modify, and distribute the software, provided you retain the original copyright notices.