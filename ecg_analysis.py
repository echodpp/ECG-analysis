import csv
import logging
import math
from ecgdetectors import Detectors


def read_data(filename):
    """
    It reads a CSV file and returns the time and voltage data
    :param filename: the name of the file to be read
    :return:
        list: time data
        list: voltage data
        list: voltages that exceeding +/- 300 mV
    """

    with open(filename, newline="") as csvfile:
        ecgreader = csv.reader(csvfile, delimiter=" ")
        time, voltage, high_voltages = parse_data(ecgreader, filename)
    return time, voltage, high_voltages


def parse_data(filereader, file):
    """
    "Parses input file data into time and voltage lists."
    The raw CSV ECG data must be read and bad values noted,
    including missing values, strings, NaNs, and voltages
    exceeding +/- 300 mV.
    :param filereader: the csv.reader object
    :param filename: The name of the file to be read
    :return: a list of time values, a list of voltage values,
    and a list of voltages exceeding +/- 300 mV.
    """

    logging.basicConfig(filename=file[10:]+'.log',
                        filemode="w", level=logging.INFO)
    time = list()
    voltage = list()
    high_voltages = list()
    for row in filereader:
        for r in row:
            line = r.split(",")
        # missing, non-numeric string, or NAN
        try:
            t_line = float(line[0])
            v_line = float(line[1])
        except ValueError:
            logging.error("Value bad/missing")
            continue
        if math.isnan(t_line) or math.isnan(v_line):
            logging.error("Value NaN")
        else:
            time.append(t_line)
            voltage.append(v_line)
        # warning voltage outside +/- 300 mV
        if v_line > 300 or v_line < -300:
            high_voltages.append(v_line)
    if len(high_voltages) > 0:
        logging.warning("file={}:high voltages={}".format(file,
                        high_voltages))
    return time, voltage, high_voltages


def duration(time):
    """
    "Calculates time span of ECG strip data."

    :param time: the time data
    :return: The time duration of the ECG trace.
    """

    logging.info("Calculating time span of ECG trace")
    timespan = time[-1] - time[0]
    return timespan


def voltage_extremes(voltage):
    """
    "Pinpoints min and max of voltages in ECG strip data."

    The min and max voltages can provide information on
    abnormal polarization of the heart or point out abnormal
    data, whether too high or too low. Normal ECG amplitude
    reaches about 2.5-3.0 mV maximum

    :param voltage: the voltage data from the ECG strip
    :return: The min and max voltages of the ECG trace.
    """

    logging.info("Identifying voltage extremes of ECG trace")
    minv = min(voltage)
    maxv = max(voltage)
    return minv, maxv


def num_beats(time, voltage):
    """
    It takes in a voltage and time array, and returns the number of peaks
    and the indices of the peaks

    :param time: the time data
    :param voltage: the voltage data
    :return: The number of beats and the indices of the peaks
    """

    logging.info("Calculating number of beats in ECG trace")
    fs = 1 / (time[1] - time[0])
    detectors = Detectors(fs)
    unfiltered_ecg = voltage
    peaks = detectors.pan_tompkins_detector(unfiltered_ecg)
    numbeats = len(peaks)
    return numbeats, peaks


def mean_hr_bpm(numbeats, t_in_s):
    """Calculates heart rate from previously determined beats and timespan

    :param numbeats: the number of beats in the ECG strip
    :param t_in_s: the time duration of the ECG strip in seconds
    :return: The average heart rate in beats per minute.
    """

    logging.info("Calculating mean HR of ECG trace")
    t_in_min = t_in_s / 60
    bpm = round(numbeats / t_in_min)
    return bpm


def beats(peak_indices, time):
    """It takes in a list of peak indices and a list of time values,
    and returns a list of time values
    corresponding to the peak indices

    :param peak_indices: list of indices of peaks in the ECG trace
    :param time: the time data of the ECG strip
    :return: The time of the beats in the ECG trace.
    """

    logging.info("Identifying time of beats in ECG trace")
    peak_times = list()
    for i in peak_indices:
        peak_time = time[i]
        peak_times.append(peak_time)
    return peak_times


def create_dict(timespan, extremes, numbeats, mean_hr, beat_times):
    """This function takes in the timespan, extremes, numbeats,
    mean_hr, and beat_times and returns a
    dictionary with the key ECG information

    :param timespan: the duration of the ECG file in seconds
    :param extremes: the minimum and maximum voltages in the file
    :param numbeats: number of detected beats in file
    :param mean_hr: average heart rate over file length
    :param beat_times: a list of times when a beat occurred
    :return: A dictionary with the key ECG information
    """

    logging.info("Assigning dictionary entries")
    metrics = {
        "duration": timespan,
        "voltage_extremes": extremes,
        "num_beats": numbeats,
        "mean_hr_bpm": mean_hr,
        "beats": beat_times,
    }
    return metrics


def save_json(hr_dict, file):
    """
    "Saves set of ECG data's key stats in JSON format"
    ECG data is saved under 'test_data#.json' format
    with the following info: duration (float),
    voltage_extremes (float tuple), num_beats (int),
    mean_hr_bpm (int), beats (list of floats)

    :param hr_dict: a dictionary of the patient's information
    :param file: the file name and path to the CSV file
    :return: The JSON file is being returned.
    """

    import json

    logging.info("Writing JSON file")
    filepath_split = file.split("/")
    filename_csv = filepath_split[1]
    filename_stem = filename_csv.split(".")
    filename = filename_stem[0]
    filename = "{}.json".format(filename)
    out_file = open(filename, "w")
    json.dump(hr_dict, out_file)
    out_file.close()
    return out_file


def analyze(time, voltage, file):
    """
    This function takes in a time and voltage list
    and a file name and path, and returns a dictionary of
    metrics

    :param time: a list of time values
    :param voltage: list of voltage values
    :param file: the name of the file to be analyzed
    :return: A dictionary of the metrics
    """

    logging.info("Starting analysis of new ECG trace")
    timespan = duration(time)
    extremes = voltage_extremes(voltage)
    numbeats, peaks = num_beats(time, voltage)
    mean_hr = mean_hr_bpm(numbeats, timespan)
    beat_times = beats(peaks, time)
    metrics = create_dict(timespan, extremes, numbeats, mean_hr, beat_times)
    save_json(metrics, file)
    return metrics


if __name__ == "__main__":
    file = "test_data/test_data7.csv"
    time, voltage, high_voltages = read_data(file)
    analyze(time, voltage, file)
