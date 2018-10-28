import pytest
from hbAnalysis import get_data
from hbAnalysis import get_duration, get_voltage_extremes
from hbAnalysis import get_beats, get_num_beats, get_mean_hr_bpm

@pytest.mark.parametrize("test_input, expected", [
    ("unittest_data/test_data1.csv",
     [0.0, 0.003, 0.006]),
    ("unittest_data/test_data2.csv",
     [2.864, 2.867, 2.8689999999999998, 2.872]),
    ("unittest_data/test_data3.csv",
     [3.25, 3.253, 3.2560000000000002, 3.258, 3.261]),
    ("unittest_data/test_data4.csv",
     [27.653000000000002, 27.656, 27.658, 27.660999999999998, 27.664, 27.666999999999998]),
])
def test_get_data(test_input, expected):
    #print("in test_get_data")
    df = get_data(test_input)
    assert (list(df.time) == expected)


@pytest.mark.parametrize("test_input, expected", [
    ("unittest_data/test_data1.csv", 0.006),
    ("unittest_data/test_data2.csv", 2.872),
    ("unittest_data/test_data3.csv", 3.261),
    ("unittest_data/test_data4.csv", 27.666999999999998),
])
def test_get_duration(test_input, expected):
    #print("in test_get_duration")
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
    #print("in test_get_voltage_extremes")
    df = get_data(test_input)
    extremes = get_voltage_extremes(df)
    assert(extremes == expected)