import pytest
from collections import deque

def moving_average(window):
    return sum(window) / len(window) if window else 0.0

def is_in_range(value, min_val, max_val):
    return min_val <= value <= max_val

class TestSensorFilter:
    def test_moving_average_single_value(self):
        window = deque([25.0], maxlen=5)
        assert moving_average(window) == 25.0

    def test_moving_average_multiple_values(self):
        window = deque([20.0, 22.0, 24.0], maxlen=5)
        assert moving_average(window) == pytest.approx(22.0)

    def test_moving_average_full_window(self):
        window = deque([10.0, 20.0, 30.0, 40.0, 50.0], maxlen=5)
        assert moving_average(window) == pytest.approx(30.0)

    def test_window_evicts_oldest_value(self):
        window = deque([10.0, 20.0, 30.0, 40.0, 50.0], maxlen=5)
        window.append(60.0)
        assert list(window) == [20.0, 30.0, 40.0, 50.0, 60.0]

    def test_temperature_in_range(self):
        assert is_in_range(25.0, -10.0, 60.0) is True

    def test_temperature_too_high(self):
        assert is_in_range(70.0, -10.0, 60.0) is False

    def test_temperature_too_low(self):
        assert is_in_range(-20.0, -10.0, 60.0) is False

    def test_humidity_boundary_values(self):
        assert is_in_range(0.0,   0.0, 100.0) is True
        assert is_in_range(100.0, 0.0, 100.0) is True
        assert is_in_range(100.1, 0.0, 100.0) is False
