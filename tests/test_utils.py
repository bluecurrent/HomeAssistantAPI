from src.bluecurrent_api.utils import *
from datetime import datetime, timezone, timedelta


def test_calculate_total_from_phases():
    total = calculate_usage_from_phases((10, 10, 10))
    assert total == 10

    total = calculate_usage_from_phases((0, 0, 0))
    assert total == 0

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

    assert create_datetime("20010101 00:00:00") == datetime(
        2001, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
    )

    assert create_datetime("") == None


def test_handle_status():
    message = {
        "data": {
            'ch_actual_v1': 12,
            'ch_actual_v2': 14,
            'ch_actual_v3': 15,
            'ch_actual_p1': 12,
            'ch_actual_p2': 10,
            'ch_actual_p3': 15,
            'ch_activity': "charging",
            'start_datetime': "20211118 14:12:23",
            'stop_datetime': "20211118 14:32:23",
            'ch_offline_since': "20211118 14:32:23",
            'total_cost': 10.52,
            'vehicle_status': "A",
            'ch_actual_kwh': 10,
            'evse_id': "101",
        }
    }

    handle_status(message)

    assert message["data"]["ch_total_voltage"] == 13.7
    assert message["data"]["ch_total_current"] == 12.3
    assert message["data"]["start_datetime"] == datetime(
        2021, 11, 18, 14, 12, 23, tzinfo=timezone(timedelta(seconds=3600)))
    assert message["data"]["stop_datetime"] == datetime(
        2021, 11, 18, 14, 32, 23, tzinfo=timezone(timedelta(seconds=3600)))
    assert message["data"]["ch_offline_since"] == datetime(
        2021, 11, 18, 14, 32, 23, tzinfo=timezone(timedelta(seconds=3600)))
    assert message["data"]["vehicle_status"] == "standby"

    assert len(message["data"]) == 16


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
