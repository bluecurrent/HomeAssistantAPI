import asyncio
import json
import websockets
import ssl
from asyncio.exceptions import TimeoutError
from websockets.exceptions import ConnectionClosed
from .errors import WebsocketError
from .utils import handle_grid, handle_status

default_objects = ["STATUS", "CHARGE_POINTS", "GRID", "SETTINGS"]

class Websocket:
    _connection = None
    _has_connection = False
    token = None
    receiver = None

    def __init__(self):
        pass

    async def validate_token(self, token, url):
        await self.connect(token, url)
        await self.send_request({"command": "VALIDATE_TOKEN"})
        res = await self._recv()
        # check result
        await self.disconnect()
        
        return True # temp

    async def get_charge_cards(self, token, url):
        await self.connect(token, url)
        await self.send_request({"command": "GET_CARDS"})
        res = await self._recv()
        await self.disconnect()
        return res


    def set_on_data(self, on_data):
        self.on_data = on_data

    async def connect(self, token, url):

        #needed for wss
        def get_ssl():
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            return ssl_context
        
        # disconnect and raise an WebSocketError when an connection already exists
        if self._has_connection:
            await self.disconnect()
            raise WebsocketError("Connection already exists.")

        self.token = token
        try:
            if url[:3] == 'wss':
                self._connection = await websockets.connect(url, ssl=get_ssl())
            else:
                self._connection = await websockets.connect(url)
            self._has_connection = True
        except (ConnectionRefusedError, TimeoutError) as err:
            raise WebsocketError("Cannot connect to the websocket.", err)

    async def send_request(self, request, receiver=None):

        async def check_receiver():
            if self.receiver is not None and self._has_connection:
                await asyncio.sleep(0.1)
                await check_receiver()
            else:
                return

        if not self.token:
            raise AttributeError('token not set')

        request['Authorization'] = self.token

        if receiver:
            await check_receiver()

            self.receiver = receiver
        await self._send(request)

    async def loop(self):
        while True:

            message: dict = await self._recv()

            if not message:
                break

            elif message.get('error') is not None:
                raise WebsocketError(message.get('error'))

            elif message["object"] not in default_objects:
                if self.receiver:
                    self.receiver(message)
                    self.receiver = None
            else:
                if message["object"] == "STATUS":
                    handle_status(message)
                elif message["object"] == "GRID":
                    handle_grid(message)
                #todo
                await self.on_data(message)


    # json
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

            # needed for when disconnect gets called. 
            # Because of the await on self._connection.close() python runs ths method. ConnectionClosed gets called
            # and the WebsocketError is raised but because of the sleep python goes back to the the disconnect, 
            # finished it and this method now sees that has_connection is False.
            # await asyncio.sleep(0.1)

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
            raise WebsocketError("Connection never started.")