import asyncio
import json
import websockets
import ssl
from asyncio.exceptions import TimeoutError
from websockets.exceptions import ConnectionClosed
from .errors import WebsocketError

default_objects = ["STATUS", "CHARGE_POINTS", "GRID_STATUS"]

class Websocket:
    _connection = None
    token = None
    receiver = None


    def __init__(self):
        pass

    async def validate_token(self, token, url):
        await self.connect(token, url)
        await self.send_request({"command": "VALIDATE_TOKEN"})
        res = await self._recv()
        await self.disconnect()
        return bool(res['data'])


    def set_on_data(self, on_data):
        self.on_data = on_data

    # connect to api
    async def connect(self, token, url):
        self.token = token
        try:
            if url[:3] == 'wss':
                self._connection = await websockets.connect(url, ssl=self.get_ssl())
            else:
                self._connection = await websockets.connect(url)
        except (ConnectionRefusedError, TimeoutError) as err:
            print(err)
            raise WebsocketError("cannot connect to the websocket", err)

    def get_ssl():
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    async def send_request(self, request, receiver=None):

        if not self.token:
            raise AttributeError('token not set')

        request['Authorization'] = self.token

        if receiver:
            self.receiver = receiver
        await asyncio.sleep(0.1)
        await self._send(request)

    async def loop(self):
        while True:
            
            message: dict = await self._recv()

            # loop still has to work so the error needs to be handled inside on_data
            # if "error" in message:
            #     raise WebsocketError(message["error"])

            message

            # TODO
            # check if auth ok ! raise invalidToken
            
            if message["object"] not in default_objects:
                if self.receiver:
                    self.receiver(message)
                    self.receiver = None
            else:
                self.on_data(message)

    # json
    async def _send(self, data):
        try:
            self.check_connection()
            data = json.dumps(data)
            await self._connection.send(data)
        except WebsocketError:
            pass

    async def _recv(self):
        try:
            self.check_connection()
            data = await self._connection.recv()
            return json.loads(data)
        except ConnectionClosed:
            self._connection = None
            raise WebsocketError("connection was closed")
        except WebsocketError:
            pass

    # close connection
    async def disconnect(self):
        try:
            self.check_connection()
            await self._connection.close()
            self._connection = None
        except WebsocketError:
            pass

    def check_connection(self):
       if not self._connection:
           raise WebsocketError("connection does not exist")