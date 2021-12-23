from .websocket import Websocket

URL = "wss://bo-acct001.bluecurrent.nl/appserver/2.0"
# URL = "wss://motown-dev2.bluecurrent.nl/appsocket"


class Client:
    def __init__(self):
        self.websocket = Websocket()
        pass

    async def validate_token(self, token, url=URL):
        return await self.websocket.validate_token(token, url)

    async def get_charge_cards(self, token, url=URL):
        return await self.websocket.get_charge_cards(token, url)

    async def connect(self, token, url=URL):
        await self.websocket.connect(token, url)

    async def start_loop(self):
        await self.websocket.loop()

    async def disconnect(self):
        await self.websocket.disconnect()

    def set_on_data(self, on_data):
        self.websocket.set_on_data(on_data)

    async def get_charge_points(self):
        request = self._create_request("GET_CHARGE_POINTS")
        await self.websocket.send_request(request)

    async def get_status(self, evse_id):
        request = self._create_request("GET_CH_STATUS", evse_id)
        await self.websocket.send_request(request)

    async def get_settings(self, evse_id):
        request = self._create_request("GET_CH_SETTINGS", evse_id)
        await self.websocket.send_request(request)

    async def get_grid_status(self, evse_id):
        request = self._create_request("GET_GRID_STATUS", evse_id)
        await self.websocket.send_request(request)

    async def set_public_charging(self, evse_id, value):
        request = self._create_request("SET_PUBLIC_CHARGING", evse_id, value)
        await self.websocket.send_request(request)

    async def set_plug_and_charge(self, evse_id, value):
        request = self._create_request("SET_PLUG_AND_CHARGE", evse_id, value)
        await self.websocket.send_request(request)

    async def set_available(self, evse_id, value):
        request = self._create_request("SET_AVAILABLE", evse_id, value)
        await self.websocket.send_request(request)

    async def reset(self, evse_id):
        request = self._create_request("SOFT_RESET", evse_id)
        await self.websocket.send_request(request)

    async def reboot(self, evse_id):
        request = self._create_request("REBOOT", evse_id)
        await self.websocket.send_request(request)

    async def start_session(self, evse_id, card_uid):
        request = self._create_request(
            "START_SESSION", evse_id, card_uid=card_uid)
        await self.websocket.send_request(request)

    async def stop_session(self, evse_id):
        request = self._create_request("STOP_SESSION", evse_id)
        await self.websocket.send_request(request)

    def _create_request(self, command, evse_id=None, value=None, card_uid=None, card_id=None):

        request = {"command": command}

        if evse_id:
            request["evse_id"] = evse_id

        if value != None:
            request["value"] = value

        if card_uid:
            request["uid"] = card_uid

        if card_id:
            request["id"] = card_id

        return request
