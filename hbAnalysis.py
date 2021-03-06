"""
    This module provides the methods to get the wanted labels:
        voltage_extremes
        duration
        numb_beats
        beats
        mean_hr_bpm
"""

import pandas as pd
import numpy as np
import math
from scipy.signal import butter, lfilter # Import the extra module required


measures = {}


def get_data(filename):
    """
    This is the get_data function, which can be rewrite to read the different
    date. For this homework, the DataFrame has column names: time, volt

    Args:
        filename: path of the csv file

    Returns:
        a dataFrame has column names: time, volt

    """
    df = pd.read_csv(filename, names=['time', 'volt'])
    return df


def get_voltage_extremes(df):
    """
    This function is used to find voltage_extremes and fill the metrics dict

    Args:
        df: a dataFrame has column names: time, volt

    Returns:
        None
    """
    measures['voltage_extremes'] = (np.min(df.volt), np.max(df.volt))
    return measures['voltage_extremes']


def get_duration(df):
    """
    This function is used to find duration and fill the metrics dict

    Args:
        df: a dataFrame has column names: time, volt

    Returns:
        None
    """
    measures['duration'] = df.time[len(df.time)-1] # the last value of time col
    return measures['duration']


def get_num_beats(beats):
    """
    number of detected beats in the strip, count using a list of peaks

    Args:
        beats: the peak list returned by detect_peaks

    Returns:
        num_beats: len of the list
    """
    measures['num_beats'] = len(beats)
    return measures['num_beats']


def get_beats(df, peaks):
    """
    numpy array of times when a beat occurred

    Args:
        df: a dataFrame has column names: time, volt
        peaks: the peak list returned by detect_peaks

    Returns:
        numpy array of times when a beat occurred
    """
    times = df.iloc[:, 0].values
    # print("peaks is {}", peaks)
    measures['beats'] = [times[x] for x in peaks]
    # print("in get_beats, beats is {}".format(measures['beats']))
    return measures['beats']


def get_mean_hr_bpm(duration, bpm, user_input_duration):
    """
    estimated average heart rate over a user-specified number of minutes
    (can choose a default interval)

    Returns:

    """
    measures['mean_hr_bpm'] = user_input_duration / duration * bpm
    return measures['mean_hr_bpm']


def calc_fs(df):
    """
    To calculate sampling frequency, divided the number of sampled volt by time

    Args:
        df: a dataFrame has column names: time, volt
        duration:

    Returns:
        sampling frequency
    """
    fs = len(df.volt) / df.time[len(df.time)-1]
    return fs


def calc_rolling_mean(df, hrw, fs):
    """
    Calculate the moving average

    Args:
        df: a dataFrame has column names: time, volt
        hrw: half rolling window
        fs: sampling frequency

    Returns:
        none ( add a column in the dataFrame )
    """
    mov_avg = df['volt'].rolling(int(hrw*fs)).mean()
    avg_hr = (np.mean(df.volt))
    mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
    df['rolling_mean'] = mov_avg
    return [x for x in df.rolling_mean]


def calc_rr(df, peaks):
    """
    calculate interval between r and r component
    
    Args:
        df: a dataFrame has column names: time, volt
        peaks: index of r component

    Returns:
        list of intervals between r and r component
    """
    measures['rr_list'] = np.diff([x for x in df.time[peaks]])
    return measures['rr_list']


def calc_bpm(rr_list):
    """
    calculate beats per minutes
    Args:
        rr_list: list of intervals between r and r component

    Returns:
        beats per minutes
    """
    measures['bpm'] = 60 / np.mean(rr_list)
    return measures['bpm']


def calc_rrsd(rr_list):
    """
    calculate sd of intervals between r and r component
    
    Args:
        rr_list: list of intervals between r and r component

    Returns:
        list of sd of intervals between r and r component
    """
    measures['rrsd'] = np.std(rr_list)
    return measures['rrsd'];


def detect_peaks(df, w, rolling_mean):
    """
    Using rolling_mean to detect ROI, and label the index of the max in ROI

    Args:
        df: a dataFrame has column names: time, volt
        w: weight to raise the rolling mean
        rolling_mean:
    Returns:
        list of index of detected r-component
    """
    # raise moving average
    rolling_mean = [(x+((x/100)*w)) for x in rolling_mean]
    window = []
    peaks = []
    cnt = 0
    for volt in df.volt:
        mean = rolling_mean[cnt]
        # If no detectable R-complex activity -> do nothing
        if (volt <= mean) and (len(window) <= 1):
            continue
        # If signal comes above local mean, mark ROI
        elif volt > mean:
            window.append(volt)
        # If signal drops below local mean -> determine highest point
        else:
            r_component_index = cnt - len(window) + (window.index(max(window)))
            peaks.append(r_component_index)  # Add detected peak to list
            window = []  # Clear marked ROI
        cnt += 1

    return peaks


def fit_peaks(df):
    """
    move the rolling mean to optimize the peak finding

    Args:
        df: a dataFrame has column names: time, volt

    Returns:

    """
    # list with moving average raise percentages,
    w_list = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120,
              130, 140, 150, 160, 170, 180]
    w_valid = []

    hrw = 0.25
    fs = calc_fs(df)
    rolling_mean = calc_rolling_mean(df, hrw, fs)
    # detect peaks with all percentages
    for w in w_list:
        peaks = detect_peaks(df, w, rolling_mean)
        rr_list = calc_rr(df, peaks)
        bpm = calc_bpm(rr_list)
        rrsd = calc_rrsd(rr_list)
        if (rrsd > 1) and ((bpm > 30) and (bpm < 130)):
            w_valid.append([rrsd, w])

    # detect peaks with 'w' that goes with lowest rrsd
    w_best = min(w_valid, key=lambda t: t[0])[1]
    measures['peaks'] = detect_peaks(df, w_best, rolling_mean)
    return measures['peaks'], w_best


def process(df, metrics):
    raw_input = input('Enter your input:')
    input_duration = float(raw_input)

    peaks, w_best = fit_peaks(df)
    print("w_best is {}".format(w_best))
    get_voltage_extremes(df)
    get_duration(df)
    get_beats(df, peaks)
    get_num_beats(measures['beats'])
    get_mean_hr_bpm(measures['duration'],
                    calc_bpm(measures['rr_list']),
                    input_duration)

    metrics['peaks'] = measures['peaks']
    metrics['bpm'] = measures['bpm']
    metrics['voltage_extremes'] = measures['voltage_extremes']
    metrics['duration'] = measures['duration']
    metrics['beats'] = measures['beats']
    metrics['num_beats'] = measures['num_beats']
    metrics['mean_hr_bpm'] = measures['mean_hr_bpm']

    # beats = metrics['beats']
    # print("in process: beats is {}".format(get_beats(df, peaks)))


