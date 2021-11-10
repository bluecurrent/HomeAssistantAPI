from src.bluecurrent_api.errors import WebsocketError
from src.bluecurrent_api.client import Client
import pytest

def test_create_request():
    client = Client()
    client.websocket.token = '123'
    request = client.create_request("GET_CHARGEPOINTS")
    assert request == {'command': 'GET_CHARGEPOINTS'}

    request = client.create_request("GET_STATUS", '101')
    assert request == {'command': 'GET_STATUS', 'evse_id': '101'}

    request = client.create_request("SET_PLUG_AND_CHARGE", '101', True)
    assert request == {'command': 'SET_PLUG_AND_CHARGE', 'evse_id': '101', 'setting_value': True}

    request = client.create_request("STOP_SESSION", '101', card_id='1234')
    assert request == {'command': 'STOP_SESSION', 'evse_id': '101', 'card_id': '1234'}


def test_set_on_data():
    client = Client()
    client.set_on_data(print)
    assert client.websocket.on_data == print


# @pytest.mark.asyncio
# async def test_server_down():

#     client = Client()
#     with pytest.raises(WebsocketError) as err:
#         await client.connect('123', 'ws://172.29.165.154')





