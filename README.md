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
pip install bluecurrent_api
```

### Api token
using this library requires an Blue Current api token. You can generate one in the Blue Current portal

## Example

```python
from bluecurrent_api import Client
import asyncio


async def main():
    token = 'test_api_token'
    client = Client()

    # data receiver
    def on_data(data):
        print('received: ', data)

    # set the receiver method
    client.set_receiver(on_data)

    # connect to the websocket
    await client.connect(token)

    # example requests
    async def requests():
        await client.get_charge_points()
        await client.get_status('EVSE_ID')

        await client.await_receiver_event()
        await client.disconnect()

    # start the loop and send requests
    await asyncio.gather(
        client.start_loop(),
        requests()
    )

asyncio.run(main())
```

## Implemented methods

#### await await_receiver_event()
- Waits until the next message is received.

#### await validate_token(api_token)
- Validates the given token.

#### await get_charge_cards(auth_token)
- returns the users charge cards.

<sub>The methods validate_token and get_charge_cards are to be used before connecting to the websocket with connect().<sub>

#### await connect(auth_token)
- Connects to the websocket.

#### set_receiver(receiver)
- Sets the receiver method.

#### await start_loop()
- Starts the receiver loop.

#### await disconnect()
- Stops the connection.

#### await get_charge_points()
- Gets the chargepoints 

#### await get_status(evse_id)
- Gets the status from an charge point.

#### await get_settings(evse_id)
- Gets the setting states from an charge point.

#### await get_grid_status(evse_id)
- Gets the grid status from an charge point.

#### await set_public_charging(evse_id, value)
- Sets public charging to True or False.

#### await set_plug_and_charge(evse_id, value)
- Sets plug and charge to True or False.

#### await set_available(evse_id, value)
- Sets operative to True or False.

#### await reset(evse_id)
- Resets the chargepoint.

#### await reboot(evse_id)
- Reboots the chargepoint.

#### await start_session(evse_id card_uid)
- Starts a charge session.

#### await stop_session(evse_id)
- Stops a charge session.