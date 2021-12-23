import asyncio
import json
import websockets
import ssl
from asyncio.exceptions import TimeoutError
from websockets.exceptions import ConnectionClosed
from .errors import InvalidToken, WebsocketError, NoCardsFound
from .utils import handle_grid, handle_status


class Websocket:
    _connection = None
    _has_connection = False
    token = None
    on_data = None

    def __init__(self):
        pass

    async def validate_token(self, token, url):
        await self.connect(token, url)
        await self.send_request({"command": "VALIDATE_TOKEN"})
        res = await self._recv()
        if not res["success"]:
            raise InvalidToken(res['error'])
        await self.disconnect()
        return True

    async def get_charge_cards(self, token, url):
        await self.connect(token, url)
        await self.send_request({"command": "GET_CARDS"})
        res = await self._recv()
        cards = res["cards"]
        if len(cards) == 0:
            raise NoCardsFound()
        await self.disconnect()
        return cards

    def set_on_data(self, on_data):
        self.on_data = on_data
        self.is_coroutine = asyncio.iscoroutinefunction(on_data)

    async def connect(self, token, url):

        # Needed for wss.
        def get_ssl():
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            return ssl_context

        if self._has_connection:
            raise WebsocketError("Connection already started.")

        self.token = token

        try:
            if url[:3] == 'wss':
                self._connection = await websockets.connect(url, ssl=get_ssl())
            else:
                self._connection = await websockets.connect(url)
            self._has_connection = True
        except (ConnectionRefusedError, TimeoutError) as err:
            raise WebsocketError("Cannot connect to the websocket.", err)

    async def send_request(self, request):
        if not self.on_data:
            raise WebsocketError("on_data method not set")
        if not self.token:
            raise WebsocketError('token not set')

        request['authorization'] = self.token
        await self._send(request)

    async def loop(self):
        if not self.on_data:
            raise WebsocketError("on_data method not set")

        while True:
            await self._message_handler()

    async def _message_handler(self):
        message: dict = await self._recv()
        if not message:
            return
        # todo
        # elif message.get('error') is not None:
        #     raise WebsocketError(message.get('error'))

        elif not message.get("object"):
            raise WebsocketError("Received message has no object.")
        elif message["object"] == "CH_STATUS":
            handle_status(message)
        elif message["object"] == "GRID_STATUS":
            handle_grid(message)

        # Checks if await is needed.
        if self.is_coroutine:
            await self.on_data(message)
        else:
            self.on_data(message)

    async def _send(self, data):
        self.check_connection()
        try:
            data = json.dumps(data)
            await self._connection.send(data)
        except ConnectionClosed:
            if self._has_connection:
                self._has_connection = False
                raise WebsocketError("SEND connection was closed.")

    async def _recv(self):
        self.check_connection()
        try:
            data = await self._connection.recv()
            return json.loads(data)
        except ConnectionClosed:
            if self._has_connection:
                self._has_connection = False
                raise WebsocketError("RECV connection was closed.")

    async def disconnect(self):
        self.check_connection()
        if not self._has_connection:
            raise WebsocketError("Connection is already closed.")
        self._has_connection = False
        await self._connection.close()

    def check_connection(self):
        if not self._connection:
            raise WebsocketError("No connection with the api.")
