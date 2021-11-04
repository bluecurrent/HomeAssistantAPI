from src.bluecurrent_api.utils import *


def test_calculate_total_from_phases():
    total = calculate_usage_from_phases((10, 10, 10))
    assert total == 10

    total = calculate_usage_from_phases((10, None, 20))
    assert total == 15

    total = calculate_usage_from_phases((10, 6, 10))
    assert total == 8.7

    total = calculate_usage_from_phases((10, 8, 1))
    assert total == 6.3

    total = calculate_usage_from_phases((10, 0, 20))
    assert total == 15

    total = calculate_usage_from_phases((5, 0, 0))
    assert total == 5

def test_get_vehicle_status():
    assert get_vehicle_status("A") == "standby"
    assert get_vehicle_status("B") == "vehicle detected"
    assert get_vehicle_status("C") == "ready"
    assert get_vehicle_status("D") == "with ventialtion"
    assert get_vehicle_status("E") == "no power"
    assert get_vehicle_status("F") == "error"

def test_handle_status():
    message = {
        "data": {
            "voltage 1": 12,
            "voltage 2": 6,
            "voltage 3": 12,
            "current 1": 12,
            "current 2": 6,
            "current 3": 6,
            "vehicle_status": "A"
        }
    }

    result = handle_status(message)

    assert result["data"]["total voltage"] == 10
    assert result["data"]["total current"] == 8
    assert result["data"]["vehicle_status"] == "standby"