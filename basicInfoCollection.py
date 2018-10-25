import pandas as pd
import numpy as np


metrics = {}


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
    metrics['voltage_extremes'] = (np.min(df.volt), np.max(df.volt))
    return metrics['voltage_extremes']


def get_duration(df):
    """
    This function is used to find duration and fill the metrics dict

    Args:
        df: a dataFrame has column names: time, volt

    Returns:
        None
    """
    metrics['duration'] = df.time[len(df.time)-1] # the last value of time col
    return metrics['duration']

