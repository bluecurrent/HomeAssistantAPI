from datetime import datetime as dt, timedelta
from src.bluecurrent_api.utils import *


def test_calculate_total_from_phases():
    total = calculate_usage_from_phases((10, 10, 10))
    assert total == 10

    total = calculate_usage_from_phases((10, None, 20))
    assert total == 15

    total = calculate_usage_from_phases((10, 0, 20))
    assert total == 15

    total = calculate_usage_from_phases((5, 0, 0))
    assert total == 5

def test_calculate_watt():
    wh = calculate_watt(10, 10)
    assert wh == 100

    wh = calculate_watt(0, 10)
    assert wh == 0

def test_handle_status():
    message = {
        "data": {
            "voltage 1": 12,
            "voltage 2": 6,
            "voltage 3": 12,
            "current 1": 12,
            "current 2": 6,
            "current 3": 6,
        }
    }

    result = handle_status(message)

    assert result["data"]["total voltage"] == 10
    assert result["data"]["total current"] == 8
    assert result["data"]["total wh"] == 80