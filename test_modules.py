import pytest
import numpy as np
from hbAnalysis import get_data
from hbAnalysis import get_duration, get_voltage_extremes
from hbAnalysis import calc_fs, calc_rolling_mean
from hbAnalysis import detect_peaks
from hbAnalysis import calc_rr, calc_bpm, calc_rrsd
from hbAnalysis import fit_peaks
from hbAnalysis import get_beats, get_num_beats, get_mean_hr_bpm


@pytest.mark.parametrize("test_input, expected", [
    ("unittest_data/test_data1.csv",
     [0.0, 0.003, 0.006]),
    ("unittest_data/test_data2.csv",
     [2.864, 2.867, 2.8689999999999998, 2.872]),
    ("unittest_data/test_data3.csv",
     [3.25, 3.253, 3.2560000000000002, 3.258, 3.261]),
    ("unittest_data/test_data4.csv",
     [27.653000000000002, 27.656, 27.658,
      27.660999999999998, 27.664, 27.666999999999998]),
])
def test_get_data(test_input, expected):
    df = get_data(test_input)
    assert (list(df.time) == expected)


@pytest.mark.parametrize("test_input, expected", [
    ("unittest_data/test_data1.csv", 0.006),
    ("unittest_data/test_data2.csv", 2.872),
    ("unittest_data/test_data3.csv", 3.261),
    ("unittest_data/test_data4.csv", 27.666999999999998),
])
def test_get_duration(test_input, expected):
    df = get_data(test_input)
    duration = get_duration(df)
    assert(duration == expected)


@pytest.mark.parametrize("test_input, expected", [
    ("unittest_data/test_data1.csv", (-0.145, -0.145)),
    ("unittest_data/test_data2.csv", (-0.39, -0.365)),
    ("unittest_data/test_data3.csv", (-0.265, -0.235)),
    ("unittest_data/test_data4.csv", (-0.415, -0.385)),
])
def test_get_voltage_extremes(test_input, expected):
    df = get_data(test_input)
    extremes = get_voltage_extremes(df)
    assert(extremes == expected)


@pytest.mark.parametrize("test_input, expected", [
    ("unittest_data/test_calc_fs.csv", 10),
])
def test_calc_fs(test_input, expected):
    df = get_data(test_input)
    fs = calc_fs(df)
    assert(fs == expected)


@pytest.mark.parametrize("test_input, expected", [
    ("unittest_data/test_calc_rolling_mean.csv", [6.36150185,
                                                  7.666060832,
                                                  6.887545068,
                                                  3.456164586,
                                                  4.986862071]),
])
def test_calc_rolling_mean(test_input, expected):
    df = get_data(test_input)
    hrw = 1
    fs = 2
    rolling_mean = calc_rolling_mean(df, hrw, fs)
    print("rolling_mean is :{}".format(rolling_mean))
    is_close = np.std(np.array(rolling_mean) - np.array(expected))
    print("isClose is :{}".format(is_close))
    assert(is_close <= 0.001)


@pytest.mark.parametrize("test_input, expected", [
    ("test_data/test_data1.csv", [14, 75]),
])
def test_detect_peaks(test_input, expected):
    df = get_data(test_input)
    fs = calc_fs(df)
    rolling_mean = calc_rolling_mean(df, 0.25, fs)
    num_peaks = len(detect_peaks(df, 60, rolling_mean))
    minimum, maximum = expected
    print("fs is {}".format(fs))
    print("num of peaks is {}".format(num_peaks))
    assert(minimum <= num_peaks <= maximum)


@pytest.mark.parametrize("test_input, expected", [
    ("test_data/test_data1.csv", [0.3, 4]),
])
def test_calc_rr(test_input, expected):
    df = get_data(test_input)
    fs = calc_fs(df)
    rolling_mean = calc_rolling_mean(df, 0.25, fs)
    peaks = detect_peaks(df, 100, rolling_mean)
    rr_list = calc_rr(df, peaks)
    minimum, maximum = expected
    rr_list_invalid = list(filter(lambda rr: rr <= minimum or rr >= maximum,
                                  rr_list))
    print("num of peaks is {}".format(len(peaks)))
    print("num of rr_invalid is {}".format(len(rr_list_invalid)))
    assert(len(rr_list_invalid) <= 5)


@pytest.mark.parametrize("test_input, expected", [
    ("test_data/test_data1.csv", [30, 130]),
])
def test_calc_bpm(test_input, expected):
    df = get_data(test_input)
    fs = calc_fs(df)
    rolling_mean = calc_rolling_mean(df, 0.25, fs)
    peaks = detect_peaks(df, 100, rolling_mean)
    rr_list = calc_rr(df, peaks)
    bpm = calc_bpm(rr_list)
    minimum, maximum = expected
    print("bpm is {}".format(bpm))
    assert(minimum <= bpm <= maximum)


@pytest.mark.parametrize("test_input, expected", [
    ("test_data/test_data1.csv", [0.3, 2.0]),
])
def test_calc_rrsd(test_input, expected):
    df = get_data(test_input)
    fs = calc_fs(df)
    rolling_mean = calc_rolling_mean(df, 0.25, fs)
    peaks = detect_peaks(df, 100, rolling_mean)
    rr_list = calc_rr(df, peaks)
    rrsd = calc_rrsd(rr_list)
    minimum, maximum = expected
    print("rrsd is {}".format(rrsd))
    assert(minimum <= rrsd <= maximum)


@pytest.mark.parametrize("test_input, expected", [
    ("test_data/test_data1.csv", [10, 75]),
])
def test_fit_peaks(test_input, expected):
    df = get_data(test_input)
    peaks, w_best = fit_peaks(df)
    num_peaks = len(peaks)
    minimum, maximum = expected
    print("num of peaks is {}".format(num_peaks))
    print("best weight is {}".format(w_best))
    assert (minimum <= num_peaks <= maximum)


@pytest.mark.parametrize("test_input, expected", [
    ("test_data/test_data1.csv", [10, 160]),
])
def test_get_beats(test_input, expected):
    df = get_data(test_input)
    peaks, _ = fit_peaks(df)
    beats = get_beats(df, peaks)
    num_beats = len(beats)
    minimum, maximum = expected
    print("num of beats is {}".format(num_beats))
    print("beats is {}".format(beats))
    assert(minimum <= num_beats <= maximum)


# @pytest.mark.parametrize("test_input, expected", [
#     ("test_data/test_data1.csv", [10, 160]),
# ])
# def get_num_beats(test_input, expected):
#     df = get_data(test_input)
#     peaks, _ = fit_peaks(df)
#     beats = get_beats(df, peaks)
#     num_beats = get_num_beats(beats)
#     minimum, maximum = expected
#     print("num of beats is {}".format(num_beats))
#     assert (minimum <= num_beats <= maximum)
#
#
# @pytest.mark.parametrize("test_input, expected", [
#     ("test_data/test_data1.csv", [10, 160])
# ])
# def get_mean_hr_bpm(test_input, expected):
#     raw_input = input('Enter your input:')
#     input_duration = float(raw_input)
#     df = get_data(test_input)
#     duration = get_duration(df)
#     fs = calc_fs(df)
#     rolling_mean = calc_rolling_mean(df, 0.25, fs)
#     peaks = detect_peaks(df, 100, rolling_mean)
#     rr_list = calc_rr(df, peaks)
#     bpm = calc_bpm(rr_list)
#     mean_hr_bpm = get_mean_hr_bpm(duration, bpm, input_duration)
#     minimum, maximum = expected
#     print("mean_hr_bpm is {}".format(mean_hr_bpm))
#     assert (minimum <= mean_hr_bpm <= maximum)
