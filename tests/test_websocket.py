from unittest.mock import AsyncMock
from src.bluecurrent_api.websocket import Websocket
from src.bluecurrent_api.errors import WebsocketError, InvalidToken, NoCardsFound
from asyncio.exceptions import TimeoutError
import pytest
from pytest_mock import MockerFixture
from websockets.exceptions import ConnectionClosed


@pytest.mark.asyncio
async def test_validate_token(mocker: MockerFixture):
    api_token = '123'
    websocket = Websocket()
    mocker.patch('src.bluecurrent_api.websocket.Websocket._connect')
    mocker.patch('src.bluecurrent_api.websocket.Websocket._send')
    mocker.patch('src.bluecurrent_api.websocket.Websocket.disconnect')

    mocker.patch('src.bluecurrent_api.websocket.Websocket._recv',
                 return_value={"object": "STATUS_API_TOKEN", "success": True, "token": "abc"})
    result = await websocket.validate_api_token(api_token)
    assert result == True
    assert websocket.auth_token == "Token abc"

    error = 'this is an error'
    mocker.patch('src.bluecurrent_api.websocket.Websocket._recv',
                 return_value={"object": "STATUS_API_TOKEN", "success": False, 'error': error})
    with pytest.raises(InvalidToken) as err:
        await websocket.validate_api_token(api_token)
        assert err.value.message == error


@pytest.mark.asyncio
async def test_get_charge_cards(mocker: MockerFixture):
    websocket = Websocket()
    mocker.patch('src.bluecurrent_api.websocket.Websocket._connect')
    mocker.patch('src.bluecurrent_api.websocket.Websocket._send')
    mocker.patch('src.bluecurrent_api.websocket.Websocket.disconnect')

    mocker.patch('src.bluecurrent_api.websocket.Websocket._recv',
                 return_value={"object": "CHARGE_CARDS", "cards": []})

    with pytest.raises(WebsocketError):
        await websocket.get_charge_cards()
    websocket.auth_token = '123'
    with pytest.raises(NoCardsFound):
        await websocket.get_charge_cards()

    cards = [{"name": "card_1", "uid": "1234", "id": "abc"}]
    mocker.patch('src.bluecurrent_api.websocket.Websocket._recv',
                 return_value={"object": "CHARGE_CARDS", "cards": cards})
    result = await websocket.get_charge_cards()
    assert result == cards


def test_set_receiver():
    websocket = Websocket()

    def receiver():
        pass

    async def async_receiver():
        pass

    websocket.set_receiver(receiver)
    assert websocket.receiver == receiver
    assert websocket.receiver_is_coroutine == False

    websocket.set_receiver(async_receiver)
    assert websocket.receiver == async_receiver
    assert websocket.receiver_is_coroutine == True


@pytest.mark.asyncio
async def test_connect(mocker: MockerFixture):
    websocket = Websocket()
    api_token = '123'

    websocket._has_connection = True
    with pytest.raises(WebsocketError):
        await websocket.connect(api_token)


@pytest.mark.asyncio
async def test__connect(mocker: MockerFixture):
    websocket = Websocket()

    mocker.patch.object(Websocket, '_connection')
    mocker.patch(
        'src.bluecurrent_api.websocket.websockets.connect', create=True, side_effect=ConnectionRefusedError)
    with pytest.raises(WebsocketError):
        await websocket._connect()
    mocker.patch(
        'src.bluecurrent_api.websocket.websockets.connect', create=True, side_effect=TimeoutError)
    with pytest.raises(WebsocketError):
        await websocket._connect()


@pytest.mark.asyncio
async def test_send_request(mocker: MockerFixture):
    websocket = Websocket()
    mock_send = mocker.patch.object(Websocket, '_send')

    # without receiver
    with pytest.raises(WebsocketError):
        await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    websocket.receiver = mocker.Mock()

    # without token
    with pytest.raises(WebsocketError):
        await websocket.send_request({"command": "GET_CHARGE_POINTS"})

    websocket.auth_token = '123'

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

    async_mock_receiver = AsyncMock()
    websocket.set_receiver(async_mock_receiver)

    # normal flow with async receiver
    message = {"object": "CHARGE_POINTS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    async_mock_receiver.assert_called_with(message)

    mock_receiver = mocker.MagicMock()
    websocket.set_receiver(mock_receiver)

    # normal flow
    message = {"object": "CHARGE_POINTS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_receiver.assert_called_with(message)

    # ch_status flow
    message = {"object": "CH_STATUS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_status.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    # grid_status flow
    message = {"object": "GRID_STATUS"}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    await websocket._message_handler()
    mock_handle_grid.assert_called_with(message)
    mock_receiver.assert_called_with(message)

    # no object
    message = {"value": True}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(WebsocketError):
        await websocket._message_handler()

    # unknown command
    message = {"error": 0}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(WebsocketError):
        await websocket._message_handler()

    # unknown token
    message = {"error": 1}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(InvalidToken):
        await websocket._message_handler()

    # token not autorized
    message = {"error": 2}
    mocker.patch.object(Websocket, '_recv', return_value=message)
    with pytest.raises(InvalidToken):
        await websocket._message_handler()

    # unknown error
    message = {"error": 9}
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
