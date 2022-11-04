import re
from unittest import mock
from src.bluecurrent_api.utils import *
from datetime import datetime, timezone, timedelta
from pytest_mock import MockerFixture
import pytz


def test_calculate_total_from_phases():
    total = calculate_average_usage_from_phases((10, 10, 10))
    assert total == 10

    total = calculate_average_usage_from_phases((0, 0, 0))
    assert total == 0

    total = calculate_average_usage_from_phases((10, None, 20))
    assert total == 15

    total = calculate_average_usage_from_phases((10, 6, 10))
    assert total == 8.7

    total = calculate_average_usage_from_phases((10, 8, 1))
    assert total == 6.3

    total = calculate_average_usage_from_phases((10, 0, 20))
    assert total == 15

    total = calculate_average_usage_from_phases((5, 0, 0))
    assert total == 5

    total = calculate_average_usage_from_phases((6, None, None))
    assert total == 6

    total = calculate_average_usage_from_phases((None, None, None))
    assert total == 0


def test_calculate_total_kW():
    total = calculate_total_kw((14, 12, 15), 230)
    assert total == 9.43


def test_get_vehicle_status():
    assert get_vehicle_status("A") == "standby"
    assert get_vehicle_status("B") == "vehicle_detected"
    assert get_vehicle_status("C") == "ready"
    assert get_vehicle_status("D") == "ready"
    assert get_vehicle_status("E") == "no_power"
    assert get_vehicle_status("F") == "vehicle_error"


def test_create_datetime():

    TZ = pytz.timezone('Europe/Amsterdam')

    test_time = TZ.localize(datetime(
        2001, 1, 1, 0, 0, 0
    ))

    assert create_datetime("20010101 00:00:00") == test_time

    assert create_datetime("20010101 00:00:00+00:00") == datetime(
        2001, 1, 1, 0, 0, 0, tzinfo=timezone.utc
    )

    assert create_datetime("") == None


def test_handle_status():
    message = {
        "data": {
            'actual_v1': 220,
            'actual_v2': 221,
            'actual_v3': 219,
            'actual_p1': 12,
            'actual_p2': 10,
            'actual_p3': 15,
            'activity': "available",
            'start_datetime': "20211118 14:12:23",
            'stop_datetime': "20211118 14:32:23",
            'offline_since': "20211118 14:32:23",
            'total_cost': 10.52,
            'vehicle_status': "A",
            'actual_kwh': 10,
            'evse_id': 'BCU101'
        },
        "evse_id": 'BCU101'
    }

    TZ = pytz.timezone('Europe/Amsterdam')

    handle_status(message)

    assert message["data"]["avg_voltage"] == 220.0
    assert message["data"]["avg_current"] == 12.3
    assert message["data"]["total_kw"] == 8.14
    assert message["data"]["start_datetime"] == TZ.localize(datetime(
        2021, 11, 18, 14, 12, 23))
    assert message["data"]["stop_datetime"] == TZ.localize(datetime(
        2021, 11, 18, 14, 32, 23))
    assert message["data"]["offline_since"] == TZ.localize(datetime(
        2021, 11, 18, 14, 32, 23))
    assert message["data"]["vehicle_status"] == "standby"

    assert len(message["data"]) == 17


def test_handle_grid():
    message = {
        "data": {
            'grid_actual_p1': 12,
            'grid_actual_p2': 14,
            'grid_actual_p3': 15,
        }
    }

    handle_grid(message)
    assert message["data"]["grid_avg_current"] == 13.7
    assert message["data"]["grid_max_current"] == 15

    assert len(message["data"]) == 5


def test_handle_setting_change():
    message = {'object': 'STATUS_SET_PUBLIC_CHARGING',
               'result': {'setting': 'set true'}}

    handle_setting_change(message)
    assert message == {'object': 'PUBLIC_CHARGING',
                       'result': True}

    message = {'object': 'STATUS_SET_PUBLIC_CHARGING',
               'result': {'setting': 'set false'}}

    handle_setting_change(message)
    assert message == {'object': 'PUBLIC_CHARGING',
                       'result': False}


def test_handle_session_messages():

    message = {'object': 'RECEIVED_STOP_SESSION', 'success': False,
               'error': 'no active session for chargepoint: BCU101'}
    handle_session_messages(message)
    assert message == {'object': 'STOP_SESSION', 'success': False,
                       'error': 'no active session for chargepoint: BCU101'}

    message = {'object': 'STATUS_START_SESSION', 'success': False, "evse_id": "BCU101",
               'error': 'REJECTED'}
    handle_session_messages(message)
    assert message == {'object': 'START_SESSION', 'success': False, "evse_id": "BCU101",
                       'error': 'start_session rejected for chargepoint: BCU101'}

    message = {'object': 'STATUS_START_SESSION', 'success': False, "evse_id": "BCU101",
               'error': 'TIMEOUT'}
    handle_session_messages(message)
    assert message == {'object': 'START_SESSION', 'success': False, "evse_id": "BCU101",
                       'error': 'start_session timeout for chargepoint: BCU101'}

    message = {'object': 'STATUS_REBOOT', 'success': False, "evse_id": "BCU101",
               'error': 'TIMEOUT'}
    handle_session_messages(message)
    assert message == {'object': 'REBOOT', 'success': False, "evse_id": "BCU101",
                       'error': 'reboot timeout for chargepoint: BCU101'}

    message = {'object': 'STATUS_SOFT_RESET', 'success': False, "evse_id": "BCU101",
               'error': 'TIMEOUT'}
    handle_session_messages(message)
    assert message == {'object': 'SOFT_RESET', 'success': False, "evse_id": "BCU101",
                       'error': 'soft_reset timeout for chargepoint: BCU101'}


def test_get_dummy_message(mocker: MockerFixture):
    time = datetime(1901, 12, 21)
    datetime_mock = mocker.patch('src.bluecurrent_api.utils.datetime')
    datetime_mock.now = mock.Mock(return_value=time)
    assert get_dummy_message('BCU101') == {'object': 'CH_STATUS', 'data': {
        'start_datetime': time, 'evse_id': 'BCU101'}}


def test_get_next_reset_delta(mocker: MockerFixture):
    time = datetime(1901, 12, 21, 10, 30, 0)
    datetime_mock = mocker.patch('src.bluecurrent_api.utils.datetime')
    datetime_mock.now = mock.Mock(return_value=time)
    assert get_next_reset_delta() == timedelta(hours=13, minutes=30, seconds=30)
