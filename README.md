# Blue Current Api

Python wrapper for the blue current api

The library is an asyncio-driven library that interfaces with the Websocket API provided by Blue Current. This was made for the Blue Current Home Assistant integration. 

## Usage

### Requirements

Python 3.9 or newer
Python modules websockets, asyncio

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

        #different receivers
        def on_data(data):
            print('received: ', data)
     
        def a(data):
            print('a: ', data)

        # the receiver loop inside an try except to catch the connection error when the connection is stopped
        async def loop():
            try:
                await client.start_loop()
            except ConnectionError:
                print('disconnected')

        # example requests
        async def requests():
            await client.set_operative('101', True, a)
            await client.get_charge_points()
            await client.set_plug_and_charge('101', True)
            await client.disconnect()


        #store the on_data method
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

- validates the given token.

### await connect(token)

- connects to the websocket

### await disconnect()

- stops the connection

### await start_loop()

- starts the receiver loop

### set_on_data(on_data)

- sets the default method to call with new data

### await get_charge_points()

- gets the chargepoints 

### await get_status(evse_id)

- gets the status from an charge point

### await set_public_charging(evse_id, value, receiver)

- sets public charging to True or False and sends the response to the receiver

### await set_plug_and_charge(evse_id, value, receiver)

- sets plug and charge to True or False and sends the response to the receiver

### await set_operative(evse_id, value, receiver)

- sets operative to True or False and sends the response to the receiver

### await unlock_connector(evse_id)

- unlocks the connector

### await reset(evse_id)

- resets the chargepoint

### await reboot(evse_id)

- reboots the chargepoint

### await start_session(evse_id, receiver, card_id)

- starts a charge session

### await stop_session(evse_id, receiver, card_id)

- stops a charge session