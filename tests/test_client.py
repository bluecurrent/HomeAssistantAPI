from src.bluecurrent_api.client import Client
import pytest
from pytest_mock import MockerFixture


def test_create_request():
    client = Client()

    # command
    request = client._create_request("GET_CHARGE_POINTS")
    assert request == {"command": "GET_CHARGE_POINTS"}

    # evse_id
    request = client._create_request("GET_STATUS", evse_id="101")
    assert request == {"command": "GET_STATUS", "evse_id": "101"}

    # value
    request = client._create_request("SET_PLUG_AND_CHARGE", evse_id="101", value=True)
    assert request == {
        "command": "SET_PLUG_AND_CHARGE",
        "evse_id": "101",
        "value": True,
    }

    # card_uid / session_token
    request = client._create_request("START_SESSION", evse_id="101", session_token="1234")
    assert request == {
        "command": "START_SESSION",
        "evse_id": "101",
        "session_token": "1234",
    }


@pytest.mark.asyncio
async def test_requests(mocker: MockerFixture):
    test_send_request = mocker.patch(
        "src.bluecurrent_api.client.Websocket.send_request"
    )
    client = Client()

    await client.get_charge_cards()
    test_send_request.assert_called_with({"command": "GET_CHARGE_CARDS", "limit": 100})

    await client.get_charge_points()
    test_send_request.assert_called_with({"command": "GET_CHARGE_POINTS"})

    await client.get_status("101")
    test_send_request.assert_called_with({"command": "GET_CH_STATUS", "evse_id": "101"})

    await client.get_settings("101")
    test_send_request.assert_called_with(
        {"command": "GET_CH_SETTINGS", "evse_id": "101"}
    )

    await client.get_grid_status("101")
    test_send_request.assert_called_with(
        {"command": "GET_GRID_STATUS", "evse_id": "101"}
    )

    await client.set_linked_charge_cards_only("101", True)
    test_send_request.assert_called_with(
        {"command": "SET_PUBLIC_CHARGING", "evse_id": "101", "value": False}
    )

    await client.set_plug_and_charge("101", True)
    test_send_request.assert_called_with(
        {"command": "SET_PLUG_AND_CHARGE", "evse_id": "101", "value": True}
    )

    await client.block("101", False)
    test_send_request.assert_called_with({"command": "SET_OPERATIVE", "evse_id": "101"})

    await client.block("101", True)
    test_send_request.assert_called_with(
        {"command": "SET_INOPERATIVE", "evse_id": "101"}
    )

    await client.reset("101")
    test_send_request.assert_called_with({"command": "SOFT_RESET", "evse_id": "101"})

    await client.reboot("101")
    test_send_request.assert_called_with({"command": "REBOOT", "evse_id": "101"})

    await client.start_session("101", "123")
    test_send_request.assert_called_with(
        {"command": "START_SESSION", "evse_id": "101", "session_token": "123"}
    )

    await client.stop_session("101")
    test_send_request.assert_called_with({"command": "STOP_SESSION", "evse_id": "101"})

    await client.set_delayed_charging("101", True)
    test_send_request.assert_called_with({"command": "SET_DELAYED_CHARGING", "evse_id": "101", "value": True})

    await client.save_scheduled_delayed_charging("101", [1, 2], "13:00", "20:00")
    test_send_request.assert_called_with(
        {
            "command": "SAVE_SCHEDULE_DELAYED_CHARGING",
            "evse_id": "101",
            "days": "[1,2]",
            "start_time": "13:00",
            "end_time": "20:00"
        }
    )

    await client.set_price_based_charging("101", True)
    test_send_request.assert_called_with({"command": "SET_PRICE_BASED_CHARGING", "evse_id": "101", "value": True})

    await client.set_price_based_settings("101", "10:00", 6.0, 2.0)
    test_send_request.assert_called_with(
        {
            "command": "SET_PRICE_BASED_SETTINGS",
            "evse_id": "101",
            "expected_departure_time": "10:00",
            "expected_kwh": "6.0",
            "minimum_kwh": "2.0"
        }
    )

    await client.override_charging_profiles("101", True)
    test_send_request.assert_called_with(
        {
            "command": "OVERRIDE_CHARGING_PROFILES",
            "evse_id": "101",
            "value": True
        }
    )

    await client.override_delayed_charging_timeout("101", True)
    test_send_request.assert_called_with(
        {
            "command": "OVERRIDE_DELAYED_CHARGING_TIMEOUT",
            "evse_id": "101",
            "value": True
        }
    )




@pytest.mark.asyncio
async def test_on_open(mocker: MockerFixture):
    test_send_request = mocker.patch(
        "src.bluecurrent_api.client.Websocket.send_request"
    )
    client = Client()

    async def on_open():
        await client.get_charge_cards()
        await client.get_charge_points()

    await client._on_open(on_open)
    test_send_request.assert_has_calls(
        [
            mocker.call(
                {
                    "command": "HELLO",
                    "header": "homeassistant",
                }
            ),
            mocker.call({"command": "GET_CHARGE_CARDS", "limit": 100}),
            mocker.call({"command": "GET_CHARGE_POINTS"}),
        ]
    )
