import pytest

expected_missing = (
    [
        0.0,
        0.003,
        0.006,
        0.008,
        0.011,
        0.014,
        0.017,
        0.019,
        0.022,
        0.025,
        0.028,
        0.033,
        0.036,
        0.039,
        0.042,
        0.044,
        0.047,
        0.05,
    ],
    [
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.12,
        -0.13,
        -0.145,
        -0.16,
        -0.155,
        -0.16,
        -0.175,
        -0.18,
        -0.185,
        -0.17,
    ],
    [],
)

expected_nan = (
    [
        0.0,
        0.003,
        0.006,
        0.008,
        0.014,
        0.017,
        0.019,
        0.022,
        0.025,
        0.028,
        0.03,
        0.033,
        0.036,
        0.039,
        0.042,
        0.044,
        0.05,
        0.053,
    ],
    [
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.12,
        -0.13,
        -0.145,
        -0.15,
        -0.16,
        -0.155,
        -0.16,
        -0.175,
        -0.18,
        -0.17,
        -0.18,
    ],
    [],
)

expected_numeric = (
    [
        0.0,
        0.003,
        0.006,
        0.008,
        0.011,
        0.014,
        0.017,
        0.019,
        0.022,
        0.025,
        0.028,
        0.03,
        0.033,
        0.036,
        0.039,
        0.042,
        0.044,
        0.047,
        0.05,
    ],
    [
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.12,
        -0.13,
        -0.145,
        -0.15,
        -0.16,
        -0.155,
        -0.16,
        -0.175,
        -0.18,
        -0.185,
        -0.17,
    ],
    [],
)

expected_high_voltage = (
    [
        0.0,
        0.003,
        0.006,
        0.008,
        0.01,
        0.014,
        302.0,
        0.019,
        0.022,
        0.025,
        0.028,
        0.03,
        0.033,
        0.036,
        0.039,
        0.042,
        0.044,
        0.047,
        0.05,
        0.053,
    ],
    [
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.145,
        -0.12,
        -0.13,
        -0.145,
        -0.15,
        -0.16,
        -0.155,
        -0.16,
        -0.175,
        -0.18,
        -301.0,
        -0.17,
        -0.18,
    ],
    [-301.0],
)


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("test_data/test_missing.csv", expected_missing),
        ("test_data/test_nan.csv", expected_nan),
        ("test_data/test_numeric.csv", expected_numeric),
        ("test_data/test_high_voltage.csv", expected_high_voltage),
    ],
)
def test_read_data(filename, expected):
    from ecg_analysis import read_data

    answer = read_data(filename)
    assert answer == expected


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("test_data/test_missing.csv", expected_missing),
        ("test_data/test_nan.csv", expected_nan),
        ("test_data/test_numeric.csv", expected_numeric),
        ("test_data/test_high_voltage.csv", expected_high_voltage),
    ],
)
def test_parse_data(filename, expected):
    import csv
    from ecg_analysis import parse_data

    with open(filename, newline="") as csvfile:
        filereader = csv.reader(csvfile, delimiter=" ")
        answer = parse_data(filereader, filename)
    assert answer == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        ([0.3, 0.8, 1.1, 1.5, 1.8, 2.2, 3.4], 3.1),
        ([0, 0.2, 0.7, 5.6, 9.3, 11.6], 11.6),
        ([1.1, 1.5, 1.7, 1.9, 2.5, 3.6], 2.5),
    ],
)
def test_duration(time, expected):
    from ecg_analysis import duration

    answer = duration(time)
    assert answer == expected


@pytest.mark.parametrize(
    "voltage, expected",
    [
        ([0, 0.1, -0.5, 1.2, 2.4, -3.4, 1.0, 2.1], (-3.4, 2.4)),
        ([-0.1, 0.8, -5.3, 1.8, 3.5, -3.3, 2.4, -3.4], (-5.3, 3.5)),
        ([0, 0, 0, 0, 0], (0, 0)),
    ],
)
def test_voltage_extremes(voltage, expected):
    from ecg_analysis import voltage_extremes

    answer = voltage_extremes(voltage)
    assert answer == expected


@pytest.mark.parametrize(
    "file, expected",
    [
        ("test_data/test_data4.csv", 33),
        ("test_data/test_data5.csv", 35),
        ("test_data/test_data11.csv", 34),
        ("test_data/test_data16.csv", 25),
        ("test_data/test_data20.csv", 18),
        ("test_data/test_data22.csv", 37),
        ("test_data/test_data32.csv", 18),
    ],
)
def test_num_beats(file, expected):
    from ecg_analysis import num_beats
    from ecg_analysis import read_data

    time, voltage, high_voltages = read_data(file)
    answer, peaks = num_beats(time, voltage)
    assert answer == expected


@pytest.mark.parametrize(
    "file, expected",
    [
        ("test_data/test_data5.csv", 76),
        ("test_data/test_data11.csv", 73),
        ("test_data/test_data16.csv", 108),
        ("test_data/test_data20.csv", 78),
        ("test_data/test_data22.csv", 56),
        ("test_data/test_data32.csv", 78),
    ],
)
def test_mean_hr_bpm(file, expected):
    from ecg_analysis import mean_hr_bpm
    from ecg_analysis import read_data
    from ecg_analysis import num_beats
    from ecg_analysis import duration

    time, voltage, hv = read_data(file)
    numbeats, peaks = num_beats(time, voltage)
    t_in_s = duration(time)
    answer = mean_hr_bpm(numbeats, t_in_s)
    assert answer == expected


def test_beats():
    from ecg_analysis import beats
    from ecg_analysis import read_data
    from ecg_analysis import num_beats

    file = "test_data/test_data32.csv"
    time, voltage, hv = read_data(file)
    nbeats, peaks = num_beats(time, voltage)
    answer = beats(peaks, time)
    expected = [
        0.956,
        1.706,
        2.456,
        3.206,
        3.956,
        4.706,
        5.456,
        6.206,
        6.956,
        7.706,
        8.456,
        9.206,
        9.956,
        10.706,
        11.456,
        12.206,
        12.956,
        13.706,
    ]
    assert answer == expected


def test_create_dict():
    from ecg_analysis import create_dict

    timespan = 13.877
    extremes = (-375.0, 606.25)
    numbeats = 18
    mean_hr = 78
    beat_times = [
        0.956,
        1.706,
        2.456,
        3.206,
        3.956,
        4.706,
        5.456,
        6.206,
        6.956,
        7.706,
        8.456,
        9.206,
        9.956,
        10.706,
        11.456,
        12.206,
        12.956,
        13.706,
    ]
    answer = create_dict(timespan, extremes, numbeats, mean_hr, beat_times)
    expected = {
        "duration": 13.877,
        "voltage_extremes": (-375.0, 606.25),
        "num_beats": 18,
        "mean_hr_bpm": 78,
        "beats": [
            0.956,
            1.706,
            2.456,
            3.206,
            3.956,
            4.706,
            5.456,
            6.206,
            6.956,
            7.706,
            8.456,
            9.206,
            9.956,
            10.706,
            11.456,
            12.206,
            12.956,
            13.706,
        ],
    }
    assert answer == expected


def test_analyze():
    from ecg_analysis import read_data
    from ecg_analysis import analyze

    file = "test_data/test_data32.csv"
    time, voltage, hv = read_data(file)
    answer = analyze(time, voltage, file)
    expected = {
        "duration": 13.887,
        "voltage_extremes": (-375.0, 606.25),
        "num_beats": 18,
        "mean_hr_bpm": 78,
        "beats": [
            0.956,
            1.706,
            2.456,
            3.206,
            3.956,
            4.706,
            5.456,
            6.206,
            6.956,
            7.706,
            8.456,
            9.206,
            9.956,
            10.706,
            11.456,
            12.206,
            12.956,
            13.706,
        ],
    }
    assert answer == expected
