from typing import Callable
from .websocket import Websocket


class Client:
    def __init__(self):
        """Initialize the Client."""
        self.websocket = Websocket()

    async def wait_for_response(self):
        await self.websocket.get_receiver_event().wait()

    async def validate_api_token(self, api_token: str):
        """Validate an api_token."""
        return await self.websocket.validate_api_token(api_token)

    async def get_charge_cards(self):
        """Get the charge cards."""
        return await self.websocket.get_charge_cards()

    async def connect(self, api_token: str):
        """Connect to the websocket."""
        await self.websocket.connect(api_token)

    async def start_loop(self):
        """Start the receive loop."""
        await self.websocket.loop()

    async def disconnect(self):
        """Disconnect the websocket."""
        await self.websocket.disconnect()

    def set_receiver(self, receiver: Callable):
        """Set the receiver."""
        self.websocket.set_receiver(receiver)

    async def get_charge_points(self):
        """Get the charge points."""
        request = self._create_request("GET_CHARGE_POINTS")
        await self.websocket.send_request(request)

    async def get_status(self, evse_id: str):
        """Get the status of a charge point."""
        request = self._create_request("GET_CH_STATUS", evse_id)
        await self.websocket.send_request(request)

    async def get_settings(self, evse_id: str):
        """Get the settings of a charge point."""
        request = self._create_request("GET_CH_SETTINGS", evse_id)
        await self.websocket.send_request(request)

    async def get_grid_status(self, evse_id: str):
        """Get the grid status of a charge point."""
        request = self._create_request("GET_GRID_STATUS", evse_id)
        await self.websocket.send_request(request)

    async def set_public_charging(self, evse_id: str, value: bool):
        """Set public_charging of a charge point to a value."""
        request = self._create_request("SET_PUBLIC_CHARGING", evse_id, value)
        await self.websocket.send_request(request)

    async def set_plug_and_charge(self, evse_id: str, value: bool):
        """Set plug_and_charge of a charge point to a value."""
        request = self._create_request("SET_PLUG_AND_CHARGE", evse_id, value)
        await self.websocket.send_request(request)

    async def set_available(self, evse_id: str, value: bool):
        """Set available of a charge point to a value."""
        request = self._create_request("SET_AVAILABLE", evse_id, value)
        await self.websocket.send_request(request)

    async def reset(self, evse_id: str):
        """Reset a charge point."""
        request = self._create_request("SOFT_RESET", evse_id)
        await self.websocket.send_request(request)

    async def reboot(self, evse_id: str):
        """Reboot a charge point."""
        request = self._create_request("REBOOT", evse_id)
        await self.websocket.send_request(request)

    async def start_session(self, evse_id: str, card_uid: str):
        """Start a charge session at a charge point."""
        request = self._create_request(
            "START_SESSION", evse_id, card_uid=card_uid)
        await self.websocket.send_request(request)

    async def stop_session(self, evse_id: str):
        """Stop a charge session at a charge point."""
        request = self._create_request("STOP_SESSION", evse_id)
        await self.websocket.send_request(request)

    def _create_request(self, command, evse_id=None, value=None, card_uid=None, card_id=None):
        """Create a request."""
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
