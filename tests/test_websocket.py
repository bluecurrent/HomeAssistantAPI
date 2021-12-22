from unittest.mock import AsyncMock
from src.bluecurrent_api.websocket import Websocket
from src.bluecurrent_api.errors import WebsocketError
from asyncio.exceptions import TimeoutError
import pytest
import asyncio
from pytest_mock import MockerFixture
from websockets.exceptions import ConnectionClosed


def test_set_on_data():
    websocket = Websocket()

    def on_data():
        pass

    async def async_on_data():
        pass

    websocket.set_on_data(on_data)
    assert websocket.on_data == on_data
    assert websocket.is_coroutine == False

    websocket.set_on_data(async_on_data)
    assert websocket.on_data == async_on_data
    assert websocket.is_coroutine == True


# @pytest.mark.asyncio
# async def test_double_connect(mocker: MockerFixture):
#     client = Client()
#     websocket = client.websocket
#     websocket.token = '123'
#     websocket._has_connection = True

#     connection = DummyConnection()

#     mocker.patch.object(websocket, '_connection', connection)
#     with pytest.raises(WebsocketError):
#         await client.connect('123', '')


# @pytest.mark.asyncio
# async def test_no_connection():
#     client = Client()
#     client.websocket.token = '123'

#     with pytest.raises(WebsocketError):
#         await client.start_loop()

#     with pytest.raises(WebsocketError):
#         await client.get_status('101')

@pytest.mark.asyncio
async def test_connect(mocker: MockerFixture):
    websocket = Websocket()
    url = 'ws://172.21.107.206:8765'
    token = '123'

    websocket._has_connection = True
    with pytest.raises(WebsocketError):
        await websocket.connect(token, url)

    websocket._has_connection = False
    mocker.patch.object(Websocket, '_connection')
    mocker.patch(
        'src.bluecurrent_api.websocket.websockets.connect', create=True, side_effect=ConnectionRefusedError)
    with pytest.raises(WebsocketError):
        await websocket.connect(token, url)
    mocker.patch(
        'src.bluecurrent_api.websocket.websockets.connect', create=True, side_effect=TimeoutError)
    with pytest.raises(WebsocketError):
        await websocket.connect(token, 'wss://172.21.107.206:8765')


@pytest.mark.asyncio
async def test_send_request(mocker: MockerFixture):
    websocket = Websocket()
    mock_send = mocker.patch.object(Websocket, '_send')

    # without on_data
    with pytest.raises(WebsocketError):
        await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    websocket.on_data = mocker.Mock()

    # without token
    with pytest.raises(WebsocketError):
        await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    websocket.token = '123'

    await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    mock_send.assert_called_with(
        {"command": "GET_CHARGE_POINTS", "authorization": "123"})


@pytest.mark.asyncio
async def test_loop():
    websocket = Websocket()

    with pytest.raises(WebsocketError):
        await websocket.loop()


@pytest.mark.asyncio
async def test_message_handler(mocker: MockerFixture):

    mock_handle_status = mocker.patch(
        'src.bluecurrent_api.websocket.handle_status')
    mock_handle_grid = mocker.patch(
        'src.bluecurrent_api.websocket.handle_grid')

    websocket = Websocket()

    async_mock_on_data = AsyncMock()
    websocket.set_on_data(async_mock_on_data)

    # normal flow with async on_data
    message = {"object": "CHARGE_POINTS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    async_mock_on_data.assert_called_with(message)

    mock_on_data = mocker.MagicMock()
    websocket.set_on_data(mock_on_data)

    # normal flow
    message = {"object": "CHARGE_POINTS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_on_data.assert_called_with(message)

    # ch_status flow
    message = {"object": "CH_STATUS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_status.assert_called_with(message)
    mock_on_data.assert_called_with(message)

    # grid_status flow
    message = {"object": "GRID_STATUS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_grid.assert_called_with(message)
    mock_on_data.assert_called_with(message)

    # no object
    message = {"value": True}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(WebsocketError):
        await websocket._message_handler()


@pytest.mark.asyncio
async def test_send(mocker: MockerFixture):
    websocket = Websocket()
    websocket._has_connection = True
    mocker.patch.object(Websocket, '_connection')
    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._connection.send', create=True, side_effect=ConnectionClosed(None, None))

    with pytest.raises(WebsocketError):
        await websocket._send("test")
    assert websocket._has_connection == False


@pytest.mark.asyncio
async def test_recv(mocker: MockerFixture):
    websocket = Websocket()
    websocket._has_connection = True
    mocker.patch.object(Websocket, '_connection')
    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._connection.recv', create=True, side_effect=ConnectionClosed(None, None))

    with pytest.raises(WebsocketError):
        await websocket._recv()
    assert websocket._has_connection == False


@pytest.mark.asyncio
async def test_disconnect(mocker: MockerFixture):
    websocket = Websocket()
    websocket._has_connection = True
    mocker.patch.object(Websocket, '_connection')
    mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._connection.close', create=True, side_effect=AsyncMock())

    await websocket.disconnect()
    assert websocket._has_connection == False

# todo
# ssl
# object whitelist ?
# check_connection
# validate_token
# get_charge_cards
