from src.bluecurrent_api.utils import *
from datetime import datetime


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

    total = calculate_usage_from_phases((6, None, None))
    assert total == 6

def test_get_vehicle_status():
    assert get_vehicle_status("A") == "standby"
    assert get_vehicle_status("B") == "vehicle detected"
    assert get_vehicle_status("C") == "ready"
    assert get_vehicle_status("D") == "with ventialtion"
    assert get_vehicle_status("E") == "no power"
    assert get_vehicle_status("F") == "error"

def test_create_datetime():
    assert create_datetime("2021-11-18T14:12:23") == datetime(2021, 11, 18, 14, 12, 23)

def test_handle_status():
    message = {
        "data": {
            'actual_v1': 12,
            'actual_v2': 14,
            'actual_v3': 15,
            'actual_p1': 12,
            'actual_p2': 10,
            'actual_p3': 15,
            'activity': "charging",
            'start_session': "2021-11-18T14:12:23",
            'stop_session': "2021-11-18T14:32:23",
            'offline_since': "2021-11-18T14:32:23",
            'total_cost': 10.52,
            'vehicle_status': "A",
            'actual_kwh': 10,
            'evse_id': "101",
        }
    }

    start = message["data"]["start_session"]
    stop = message["data"]["stop_session"]
    offline = message["data"]["offline_since"]

    handle_status(message)

    assert message["data"]["total_voltage"] == 13.7
    assert message["data"]["total_current"] == 12.3
    assert message["data"]["start_session"] == datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    assert message["data"]["stop_session"] ==  datetime.strptime(stop, "%Y-%m-%dT%H:%M:%S")
    assert message["data"]["offline_since"] ==  datetime.strptime(offline, "%Y-%m-%dT%H:%M:%S")
    # assert result["data"]["session_duration"] ==  datetime.strptime(message["data"]["offline_since"], "%Y-%m-%dT%H:%M:%S")
    assert message["data"]["vehicle_status"] == "standby"

    assert len(message["data"]) == 16 # 17 = duration


def test_handle_grid():
    message = {
        "data": {
            'grid_actual_p1': 12,
            'grid_actual_p2': 14,
            'grid_actual_p3': 15,
        }
    }

    handle_grid(message)
    assert message["data"]["grid_total_current"] == 13.7

    assert len(message["data"]) == 4