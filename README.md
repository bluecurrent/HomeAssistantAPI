# Blue Current Api

Python wrapper for the blue current api

The library is an asyncio-driven library that interfaces with the Websocket API provided by Blue Current. This was made for the Blue Current Home Assistant integration. 

## Usage

### Requirements

- Python 3.9 or newer
- websockets
- asyncio

### Installation

```python
pip install blue_current_api
```

### Api token
using this library requires an Blue Current api token. You can generate one in the Blue Current portal

## Example

```python
from blue_current_api import Client
from blue_current_api.errors import ConnectionError
import asyncio

async def main():
    token = 'token'
    client = Client()

    def on_data(data):
        print('received: ', data)
    

    # the receiver loop inside an try except to catch the connection error when the connection is stopped
    async def loop():
        try:
            await client.start_loop()
        except ConnectionError:
            print('disconnected')

    # example requests
    async def requests():
        await client.get_charge_points()
        await client.get_status('BCU1111')
        await client.set_plug_and_charge('BCU1111', True)
        await client.disconnect()


    #set the on_data method
    client.set_on_data(on_data)

    #connect to the websocket
    await client.connect(token)

    #start the loop and send requests
    await asyncio.gather(
        loop(),
        requests()
    )

asyncio.run(main())
```

## Implemented methods

### await validate_token(token)

- Validates the given token.

### await get_charge_cards(token)
- Validates the given token.

### await connect(token)
- Connects to the websocket.

### set_on_data(on_data)
- Sets the on_data method.

### await start_loop()
- Starts the receiver loop.

### await disconnect()
- Stops the connection.

### set_on_data(on_data)
- Sets the default method to call with new data.

### await get_charge_points()
- Gets the chargepoints 

### await get_status(evse_id)
- Gets the status from an charge point.

### await get_settings(evse_id)
- Gets the setting states from an charge point.

### await get_grid_status(evse_id)
- Gets the grid status from an charge point.

### await set_public_charging(evse_id, value)
- Sets public charging to True or False.

### await set_plug_and_charge(evse_id, value)
- Sets plug and charge to True or False.

### await set_available(evse_id, value)
- Sets operative to True or False.

### await reset(evse_id)
- Resets the chargepoint.

### await reboot(evse_id)
- Reboots the chargepoint.

### await start_session(evse_id card_uid)
- Starts a charge session.

### await stop_session(evse_id)
- Stops a charge session.