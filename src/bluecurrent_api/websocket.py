import asyncio
import json
import websockets
import ssl
from asyncio.exceptions import TimeoutError
from websockets.exceptions import ConnectionClosed
from .errors import InvalidToken, WebsocketError, NoCardsFound
from .utils import handle_grid, handle_status

URL = "wss://bo-acct001.bluecurrent.nl/appserver/2.0"


class Websocket:
    _connection = None
    _has_connection = False
    auth_token = None
    on_data = None

    def __init__(self):
        pass

    async def validate_api_token(self, api_token):
        await self._connect()
        await self._send({"command": "VALIDATE_API_TOKEN", "token": api_token})
        res = await self._recv()
        if not res["success"]:
            await self.disconnect()
            raise InvalidToken("Invalid Token")
        await self.disconnect()
        self.auth_token = "Token " + res["token"]
        return True

    async def get_charge_cards(self):
        if not self.auth_token:
            raise WebsocketError('token not set')
        await self._connect()
        await self._send({"command": "GET_CHARGE_CARDS", "authorization": self.auth_token})
        res = await self._recv()
        cards = res["cards"]
        if len(cards) == 0:
            await self.disconnect()
            raise NoCardsFound()
        await self.disconnect()
        return cards

    def set_on_data(self, on_data):
        self.on_data = on_data
        self.is_coroutine = asyncio.iscoroutinefunction(on_data)

    async def connect(self, api_token):
        if self._has_connection:
            raise WebsocketError("Connection already started.")
        await self.validate_api_token(api_token)
        await self._connect()

    async def _connect(self):
        # Needed for wss.
        def get_ssl():
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            return ssl_context

        try:
            self._connection = await websockets.connect(URL, ssl=get_ssl())
            self._has_connection = True
        except (ConnectionRefusedError, TimeoutError) as err:
            raise WebsocketError("Cannot connect to the websocket.", err)

    async def send_request(self, request):
        if not self.on_data:
            raise WebsocketError("on_data method not set")
        if not self.auth_token:
            raise WebsocketError('token not set')

        request['authorization'] = self.auth_token
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
                raise WebsocketError("connection was closed.")

    async def _recv(self):
        self.check_connection()
        try:
            data = await self._connection.recv()
            return json.loads(data)
        except ConnectionClosed:
            if self._has_connection:
                self._has_connection = False
                raise WebsocketError("connection was closed.")

    async def disconnect(self):
        self.check_connection()
        if not self._has_connection:
            raise WebsocketError("Connection is already closed.")
        self._has_connection = False
        await self._connection.close()

    def check_connection(self):
        if not self._connection:
            raise WebsocketError("No connection with the api.")
