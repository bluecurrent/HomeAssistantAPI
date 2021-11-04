from src.bluecurrent_api.errors import WebsocketError
from src.bluecurrent_api import Client
from asyncio.exceptions import TimeoutError
import pytest
import asyncio
from pytest_mock import MockerFixture
import json
from websockets.exceptions import ConnectionClosed

URL = 'ws://172.22.197.115:8765'

class DummyConnection:
    def __init__(self):
        pass

    async def send(self, data):
        return

    async def recv(self):
        return json.dumps({'object': 'test'})

    async def close(self):
        return True

def dummy_recv(data):
    return

@pytest.mark.asyncio
async def test_connect(mocker: MockerFixture):

    client = Client()

    websocket = client.websocket

    mocker.patch('bluecurrent_api.websocket.websockets.connect', side_effect=TimeoutError('mocked error'))

    with pytest.raises(WebsocketError):
        await websocket.connect('123', 'dummy')


@pytest.mark.asyncio
async def test_send(mocker: MockerFixture):

    client = Client()
    websocket = client.websocket
    websocket.token = '123'
    connection = DummyConnection()
    
    mocker.patch.object(websocket, '_connection', connection)

    mocker.patch('src.bluecurrent_api.client.Websocket.check_connection', return_value=True)
    await client.get_status('101')


@pytest.mark.asyncio
async def test_receiver(mocker: MockerFixture):
    """Receiver should be set after given to request, and should be gone after response has been received"""

    class DummyConnection:
        called = False

        def __init__(self):
            pass

        async def send(self, data):
            return

        async def recv(self):
            if self.called:
                raise ConnectionClosed(None, None)
            self.called = True
            return json.dumps({'object': 'test'})

    client = Client()
    websocket = client.websocket
    websocket.token = '123'
    
    mocker.patch.object(websocket, '_connection', DummyConnection())
    mocker.patch('src.bluecurrent_api.client.Websocket.check_connection', return_value=True)

    await client.set_public_charging('101', True, dummy_recv)

    assert websocket.receiver == dummy_recv

    await websocket.loop()

    assert websocket.receiver == None

@pytest.mark.asyncio
async def test_request_routing(mocker: MockerFixture):

    class DummyConnection:
        next = 4

        def __init__(self):
            pass

        async def send(self, data):
            return

        async def recv(self):
            await asyncio.sleep(0.1)
            a = None
            if self.next == 3:
                raise ConnectionClosed(None, None)
            elif self.next == 0:
                a = {'object': 'SET_PUBLIC_CHARGING'}
            elif self.next == 1:
                a = {'object': 'SET_OPERATIVE'}
            
            self.next = 4
            return json.dumps(a)

        def set_next(self, next):
            self.next = next
            

    connection = DummyConnection()

    client = Client()
    websocket = client.websocket
    websocket.token = '123'
    websocket._has_connection = True

    mocker.patch.object(websocket, '_connection', connection)
    mocker.patch('src.bluecurrent_api.client.Websocket.check_connection', return_value=True)

    def a(data):
        assert data["object"] == 'SET_PUBLIC_CHARGING'

    def b(data):
        assert data["object"] == 'SET_OPERATIVE'

    async def requests():
        await client.set_operative('101', True, b)
        connection.set_next(1)
        await client.set_public_charging('101', True, a)
        connection.set_next(0)
        await client.set_operative('101', True, b)
        connection.set_next(1)
        await client.set_operative('101', True, b)
        connection.set_next(1)
        await client.set_operative('101', True, a)
        connection.set_next(0)

        websocket._has_connection = False
        connection.set_next(3)
    await asyncio.gather(requests(), websocket.loop())



@pytest.mark.asyncio
async def test_disconnect(mocker: MockerFixture):
    client = Client()
    websocket = client.websocket
    
    with pytest.raises(WebsocketError):
        await client.disconnect()


    websocket.token = '123'
    websocket._has_connection = True

    connection = DummyConnection()

    mocker.patch.object(websocket, '_connection', connection)
    mocker.patch('src.bluecurrent_api.client.Websocket.check_connection', return_value=True)
    await client.disconnect()
    with pytest.raises(WebsocketError):
        await client.disconnect()

@pytest.mark.asyncio
async def test_double_connect(mocker: MockerFixture):
    client = Client()
    websocket = client.websocket
    websocket.token = '123'
    websocket._has_connection = True

    connection = DummyConnection()

    mocker.patch.object(websocket, '_connection', connection)
    with pytest.raises(WebsocketError):
        await client.connect('123', '')

@pytest.mark.asyncio
async def test_no_connection():
    client = Client()
    client.websocket.token = '123'

    with pytest.raises(WebsocketError):
        await client.start_loop()

    with pytest.raises(WebsocketError):
        await client.get_status('101')


