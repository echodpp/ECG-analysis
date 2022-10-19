![Python application test with Github Actions](https://github.com/BME547-Fall2022/ecg-analysis-echodpp/actions/workflows/pytest_runner.yml/badge.svg)
# ECG Analysis 

Author: Echo Chen

## Overview
This project analyzes several key values of voltage-time data from ECG strips: duration, voltage extremes, number and duration of beats, and average heart rate. These values are output as JSON files for each set of ECG data. Details are as follows, regarding the data source
(See [test_data\README.md](test_data/README.md) for more details.)
* `duration` (float): time duration of the ECG strip
* `voltage_extremes` (floats): tuple in the form `(min, max)` where `min` and `max`
    are the minimum and maximum lead voltages in the file    
* `num_beats` (int): number of detected beats in the strip
* `mean_hr_bpm` (int): average heart rate over the length of the strip  
* `beats` (list of floats): list of times when a beat occurred

## Instructions
* The first step is to select the dataset, which needs to contain the path. The default dataset starts with 'test_data/' and is stored in that folder.
* Set up the virtual environment and install the files in requirements.txt.
* In the last if __name__ == "__main__" of the ecg_analysis.py file, enter the selected file and path as 'file='.
* Next run it in a virtual environment using python3
* The following will give you a log file and a JSON format file: `duration`, `voltage_extremes`, `num_beats`, `mean_hr_bpm`,  and `beats`.
* You can also visualize the data using a plot.py file

More information on this assignment can be found at <https://github.com/dward2/BME547/tree/master/Assignments/ECG_Analysis>.

## Defining Beat
The heartbeat is identified by the Pan-Tompkins detector (https://github.com/berndporr/py-ecg-detectors) using the sampling period of the ECG strip (`fs = 1/(time[1]-time[0])`). The algorithm detects QRS complexes (waves in the ECG), which consist of a downward deflection (Q), a high upward deflection (R) and another downward deflection (S). Through a series of filters (low-pass, high-pass, derivative), characteristic fast depolarizations are highlighted and background noise is removed. The resulting filtered signal is then squared to amplify the QRS depolarization. Finally, adaptive thresholding is applied to detect the peaks of the signal.

## Calculating BPM
The heart rate is calculated as the number of heartbeats per minute. The duration of the ECG strip was converted to minutes by `min = sec/60`. The number of heartbeats detected in the ECG strip is then divided by the duration in minutes (`bpm = numbeats/t_in_min`) and rounded to the nearest integer.

## License
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
