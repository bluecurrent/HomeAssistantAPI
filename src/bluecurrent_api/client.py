from .websocket import Websocket

URL = "wss://bo-acct001.bluecurrent.nl/appserver/2.0"
# URL = "wss://130.61.188.91/appsocket/2.0"
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

    async def get_status(self, evse_id):
        request = self.create_request("GET_STATUS", evse_id)
        await self.websocket.send_request(request)

    async def get_settings(self, evse_id):
        request = self.create_request("GET_SETTINGS", evse_id)
        await self.websocket.send_request(request)

    async def get_charge_points(self):
        request = self.create_request("GET_CHARGE_POINTS")
        await self.websocket.send_request(request)

    async def get_grid_status(self):
        request = self.create_request("GET_GRID_STATUS")
        await self.websocket.send_request(request)

    # switches
    async def set_public_charging(self, evse_id, value, receiver=None):
        request = self.create_request("SET_PUBLIC_CHARGING", evse_id, value)
        await self.websocket.send_request(request, receiver)
        

    async def set_plug_and_charge(self, evse_id, value, receiver=None):
        request = self.create_request("SET_PLUG_AND_CHARGE", evse_id, value)
        await self.websocket.send_request(request, receiver)

    async def set_available(self, evse_id, value, receiver=None):
        request = self.create_request("SET_AVAILABLE", evse_id, value)
        await self.websocket.send_request(request, receiver)

    async def reset(self, evse_id):
        request = self.create_request("RESET", evse_id)
        await self.websocket.send_request(request)

    async def reboot(self, evse_id):
        request = self.create_request("REBOOT", evse_id)
        await self.websocket.send_request(request)

    async def start_session(self, evse_id, card_id, receiver=None):
        request = self.create_request("START_SESSION", evse_id, card_id=card_id)
        await self.websocket.send_request(request, receiver)

    async def stop_session(self, evse_id, card_id, receiver=None):
        request = self.create_request("STOP_SESSION", evse_id, card_id=card_id)
        await self.websocket.send_request(request, receiver)

    def create_request(self, command, evse_id=None, setting_value=None, 
        session_token=None, card_id=None
    ):

        request = {"command": command}

        if session_token:
            request["session_token"] = session_token

        if evse_id:
            request["evse_id"] = evse_id

        if setting_value != None:
            request["setting_value"] = setting_value

        if card_id:
            request["card_id"] = card_id

        return request