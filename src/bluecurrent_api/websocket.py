import asyncio
import json
from typing import Callable
import websockets
import ssl
from websockets.exceptions import ConnectionClosed, InvalidStatusCode
from .errors import InvalidToken, WebsocketError, NoCardsFound
from .utils import handle_grid, handle_status

URL = "wss://bo-acct001.bluecurrent.nl/appserver/2.0"


class Websocket:
    _connection = None
    _has_connection = False
    auth_token = None
    receiver = None
    receive_event = None

    def __init__(self):
        pass

    def get_receiver_event(self):

        self._check_connection()
        if self.receive_event is None:
            self.receive_event = asyncio.Event()

        self.receive_event.clear()
        return self.receive_event
    
    async def validate_api_token(self, api_token: str):
        """Validate an api token."""
        await self._connect()
        await self._send({"command": "VALIDATE_API_TOKEN", "token": api_token})
        res = await self._recv()
        await self.disconnect()
        if not res["success"]:
            raise InvalidToken("Invalid Api Token")
        self.auth_token = "Token " + res["token"]
        return True

    async def get_charge_cards(self):
        """Get the charge cards"""
        if not self.auth_token:
            raise WebsocketError("token not set")
        await self._connect()
        await self._send({"command": "GET_CHARGE_CARDS", "authorization": self.auth_token})
        res = await self._recv()
        cards = res["cards"]
        await self.disconnect()
        if len(cards) == 0:
            raise NoCardsFound()
        return cards

    def set_receiver(self, receiver: Callable):
        """Set a receiver."""
        self.receiver = receiver
        self.receiver_is_coroutine = asyncio.iscoroutinefunction(receiver)

    async def connect(self, api_token: str):
        """Validate api_token and connect to the websocket."""
        if self._has_connection:
            raise WebsocketError("Connection already started.")
        await self.validate_api_token(api_token)
        await self._connect()

    async def _connect(self):
        """Connect to the websocket."""
        try:
            self._connection = await websockets.connect(URL)
            self._has_connection = True
        except Exception:
            raise WebsocketError("Cannot connect to the websocket.")

    async def send_request(self, request: dict):
        """Add authorization and send request."""
        if not self.receiver:
            raise WebsocketError("receiver method not set")
        if not self.auth_token:
            raise WebsocketError("auth token not set")

        request["Authorization"] = self.auth_token
        await self._send(request)

    async def loop(self):
        """Loop the message_handler."""
        if not self.receiver:
            raise WebsocketError("receiver method not set")

        while True:
            stop = await self._message_handler()
            if stop:
                break

    async def _message_handler(self):
        """Wait for a message and give it to the receiver."""
        message: dict = await self._recv()
        if not message:
            return True

        object_name = message.get("object")
        error_code = message.get("error")

        if error_code == 0:
            raise WebsocketError("Unknown command")
        elif error_code == 1:
            raise InvalidToken('Invalid Auth Token')
        elif error_code == 2:
            raise WebsocketError('Not authorized')
        elif error_code == 9:
            raise WebsocketError("Unknown error")
        elif not object_name:
            raise WebsocketError("Received message has no object.")
        elif object_name == "CH_STATUS":
            handle_status(message)
        elif object_name == "GRID_STATUS":
            handle_grid(message)

        self.handle_receive_event()
        if self.receiver_is_coroutine:
            await self.receiver(message)
        else:
            self.receiver(message)

    async def _send(self, data: dict):
        """Send data to the websocket."""
        self._check_connection()
        try:
            data_str = json.dumps(data)
            await self._connection.send(data_str)
        except (ConnectionClosed, InvalidStatusCode):
            self.handle_connection_errors()

    async def _recv(self):
        """Receive data from de websocket."""
        self._check_connection()
        try:
            data = await self._connection.recv()
            return json.loads(data)
        except (ConnectionClosed, InvalidStatusCode):
            self.handle_connection_errors()

    def handle_connection_errors(self):
        if self._has_connection:
            self._has_connection = False
            self.handle_receive_event()
            raise WebsocketError("connection was closed.")

    async def disconnect(self):
        """Disconnect from de websocket"""
        self._check_connection()
        if not self._has_connection:
            raise WebsocketError("Connection is already closed.")
        self._has_connection = False
        self.handle_receive_event()
        await self._connection.close()

    def _check_connection(self):
        """check if the connection still exists."""
        if not self._connection:
            raise WebsocketError("No connection with the api.")

    def handle_receive_event(self):
        if self.receive_event is not None:
            self.receive_event.set()