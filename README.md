# ECG Analysis Dashboard
---
![project preview](/assets/2026-03-1509-37-37-ezgif.com-video-to-gif-converter.gif)

- **Full video explanation**: https://www.youtube.com/watch?v=mEIwtYiDcGQ
---
## Summary 

>- [*Project's Stack*](#projects-stack)
>- [*Instructions*](#instructions)
>- [*How the Dashboard works*](#how-the-dashboard-works)
>- [*The Digital Processing of the ECG Signal*](#the-digital-processing-of-the-ecg-signal)
>- [*The Dashboard Architecture*](#the-dashboard-architecture)
>- [*Lincensed*](#licensed)
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

- The choice of filter order

Initially, I started working with higher order filters like 80, 90, and 100 in order to minimize the transition band between the desired frequency band for my application and the frequency band to be attenuated.

However, it was observed that as the filter order increases, the **amplitude peaks of the original signal are also attenuated**. Conversely, if the filter order is too low, the transition band would consequently be larger, and some undesirable frequency components would pass through the filter.

Therefore, I adjusted the value to best suit my application, using a 10th order filter. The comparison between these two graphs highlights my choice.

> Impact of the 100th order filter
![rawvsfiltered_order_100](/assets/raw%20vs%20filtered%20ecg%20order%20100.png)
> Impact of the 10th order filter 
![rawvsfiltered_order_10](/assets/raw%20vs%20filtered%20ecg%20order%2010%20.png)

#### ECG Signal Analysis Step

##### Energy calculation

The calculation of the total energy of a finite digital signal can be defined as follows:

$$E = \sum_{n=0}^{N-1} x[n]^2$$

Note that this calculation will be a summation of the energies of the samples contained only within the interval of a window of size *L*, varying in position by *k*. Therefore, we can define the energy of each window to be computed as follows:

$$E_k = \frac{1}{L} \sum_{n=k}^{k+L-1} x[n]^2$$

This defines the local energy of each window being the local average power.

##### Energy differences

Once we define an energy window as just an interval of the signal where we have the computed energy value, we can make this window slide through the ECG signal, iterating sample by sample in a loop where each time this window slides we will be calculating the energy difference at various points in the signal. We can represent this mathematically as follows:

$$\Delta E[n] = E[n] - E[n-1]$$

##### Detection of possible anomalies

The result of this energy variation can indicate some representations:

1. ΔE ≈ 0 → The ECG is stable
2. Large positive ΔE → If a QRS complex occurs
3. Large negative ΔE → After a QRS complex occurs

And the simple anomaly detector I made is based precisely on this idea and uses the mean and standard deviation to define the thresholds that will indicate possible anomalies.

- Mean (µ)

$$\mu=E[\Delta E]$$

Calculating the mean of the energy variation will give us the expected central level of our variation. In other words, it defines for us what the "normal" behavior of the system would be.

And the simple anomaly detector I made is based precisely on this idea and uses the mean and standard deviation to define the thresholds that will indicate possible anomalies.

- Standard Deviation (σ) 

$$\sigma = \sqrt{E[(\Delta E - \mu)^2]}$$

Calculating the standard deviation will be indispensable for us, considering that it will tell us how much the energy variations normally oscillate around the mean, that is, it defines the natural scale of fluctuation of the ECG signal. Logo:

> If σ is small:
The signal is stable. Small changes are already relevant.

> If σ is large:
The signal is naturally more variable. Larger changes are needed to consider it an anomaly.

- Thresholds

We can finally define our thresholds that will dictate anomalous events:

$$Threshold = \mu \pm k\sigma$$

The +- signs refer to the positive and negative thresholds, since the points of possible anomalies can exceed either the positive or negative values ​​limited by the thresholds.

It is important to note that *k* will be **the hyperparameter we will use to adjust the sensitivity** of anomalous event detection. We must be careful with this hyperparameter because:

> If *k* is too small: The detector becomes too sensitive, leading to an exaggerated appearance of anomalous events and creating a false-positive result, where the test detects the existence of a disease even if the patient does not have it.

> If *k* is too large: The detector has difficulty passing any point because the thresholds are too high. Therefore, we may miss anomalous events present in the signal.

--- 

### The Dashboard Architecture

To build the dashboard, I used the Streamlit Python library due to its native integration with the Python ecosystem. The goal was to avoid over-engineering the project as much as possible; that is, building a super-elaborate front-end, a distributed back-end, and creating a relational database to manage a considerably small data flow.

Although the system is not scalable, it will be sufficient for displaying data in a more academic way.

#### Streamlit's multipage architecture

In this sense, I used a multi-page architecture provided by Streamlit to build the dashboard pages.

```
pages/
    _Analysis_ECG.py
    _Home.py
    _Sign_in.py
    _Upload_ECG.py
```

As you can see, in the way it's organized, each page has a corresponding file associated with /pages, automatically becoming a route.

#### Separation of responsibilities

To avoid mixing the code, I separated it into two layers, which are worth mentioning below. The intention is to separate the interface model from the processing logic, thus improving maintainability, testability, and code organization.

- UI Layer

This layer contains the essential files for building the user interface. I'm referring to all those that, in addition to being responsible for the interface, are directly associated with the inputs and the dashboard visualization.

For example, all the files in /pages make up the UI layer.

- Processing Layer

This layer contains the files necessary to deliver the computational calculations of the dashboard to the user. I'm referring to the mathematical logic, statistics, and the detection algorithm.

#### Separation of data

I also made sure to separate the responsibilities, including the data related to the raw ECG signals from the processed ones. It was a more organized way I found to manage the metadata of the patients' ECG signals.

---

### Licensed 

This project is licensed under the ***MIT*** License. You are free to use, copy, modify, and distribute the software, provided you retain the original copyright notices.