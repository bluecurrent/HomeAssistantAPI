"""Define an object with all public methods."""
import asyncio
import json
from typing import Callable
from websockets.client import connect
from websockets.exceptions import ConnectionClosed, InvalidStatusCode
from .exceptions import InvalidApiToken, WebsocketException, NoCardsFound
from .utils import handle_status, handle_grid, handle_setting_change, handle_session_messages

URL = "wss://bo-acct001.bluecurrent.nl/appserver/2.0"


class Websocket:
    """Class for handling requests and responses for the BlueCurrent Websocket Api."""
    _connection = None
    _has_connection = False
    auth_token = None
    receiver = None
    receive_event = None
    receiver_is_coroutine = None

    def __init__(self):
        pass

    def get_receiver_event(self):
        """Returns cleared receive_event when connected."""

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
            raise InvalidApiToken
        self.auth_token = "Token " + res["token"]
        return True

    async def get_charge_cards(self):
        """Get the charge cards."""
        if not self.auth_token:
            raise WebsocketException("token not set")
        await self._connect()
        await self._send({"command": "GET_CHARGE_CARDS", "Authorization": self.auth_token})
        res = await self._recv()
        cards = res["cards"]
        await self.disconnect()
        if len(cards) == 0:
            raise NoCardsFound
        return cards

    def set_receiver(self, receiver: Callable):
        """Set a receiver."""
        self.receiver = receiver
        self.receiver_is_coroutine = asyncio.iscoroutinefunction(receiver)

    async def connect(self, api_token: str):
        """Validate api_token and connect to the websocket."""
        if self._has_connection:
            raise WebsocketException("Connection already started.")
        await self.validate_api_token(api_token)
        await self._connect()

    async def _connect(self):
        """Connect to the websocket."""
        try:
            self._connection = await connect(URL)
            self._has_connection = True
        except Exception as err:
            raise WebsocketException(
                "Cannot connect to the websocket.") from err

    async def send_request(self, request: dict):
        """Add authorization and send request."""
        if not self.receiver:
            raise WebsocketException("receiver method not set")
        if not self.auth_token:
            raise WebsocketException("auth token not set")

        request["Authorization"] = self.auth_token
        await self._send(request)

    async def loop(self):
        """Loop the message_handler."""
        if not self.receiver:
            raise WebsocketException("receiver method not set")

        await self._send({"command": "HELLO", "Authorization": self.auth_token})

        while True:
            stop = await self._message_handler()
            if stop:
                break

    async def _message_handler(self):
        """Wait for a message and give it to the receiver."""
        errors = {
            0: "Unknown command",
            1: "Invalid Auth Token",
            2: "Not authorized",
            9: "Unknown error"
        }

        message: dict = await self._recv()

        # websocket has disconnected
        if not message:
            return True

        object_name = message.get("object")
        error = message.get("error")

        if not object_name:
            raise WebsocketException("Received message has no object.")

        # ignore RECEIVED objects without error
        if "RECEIVED" in object_name and not error:
            return False

        # handle errors
        if error in errors:
            raise WebsocketException(errors[error])

        if object_name == "CH_STATUS":
            handle_status(message)
        elif object_name == "GRID_STATUS":
            handle_grid(message)
        elif "STATUS_SET_P" in object_name:
            handle_setting_change(message)
        elif "STATUS" in object_name or "RECEIVED" in object_name:
            handle_session_messages(message)

        if object_name != "HELLO":
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
        """Handle connection errors."""
        if self._has_connection:
            self._has_connection = False
            self.handle_receive_event()
            raise WebsocketException("connection was closed.")

    async def disconnect(self):
        """Disconnect from de websocket."""
        self._check_connection()
        if not self._has_connection:
            raise WebsocketException("Connection is already closed.")
        self._has_connection = False
        self.handle_receive_event()
        await self._connection.close()

    def _check_connection(self):
        """Throw error if there is no connection."""
        if not self._connection:
            raise WebsocketException("No connection with the api.")

    def handle_receive_event(self):
        "Set receive_event if it exists"
        if self.receive_event is not None:
            self.receive_event.set()
