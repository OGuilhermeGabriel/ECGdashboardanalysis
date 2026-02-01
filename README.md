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

--- 

### The Software Architecture
---

### Licensed 

This project is licensed under the ***MIT*** License. You are free to use, copy, modify, and distribute the software, provided you retain the original copyright notices.