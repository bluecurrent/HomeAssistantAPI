# Blue Current Api

Python wrapper for the blue current api

The library is a asyncio-driven library that interfaces with the Websocket API provided by Blue Current. This was made for the Blue Current Home Assistant integration.

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

using this library requires a Blue Current api token. You can generate one in your Blue Current dashboard.

## Example

```python
from bluecurrent_api import Client
import asyncio


async def main():
    api_token = 'api_token'
    client = Client()

    # data receiver
    def on_data(data):
        print('received: ', data)

    # set the receiver
    client.set_receiver(on_data)

    # connect to the websocket
    await client.connect(api_token)

    # example requests
    async def requests():
        await client.get_charge_points()
        await client.wait_for_response()
        await client.disconnect()

    # start the loop and send requests
    await asyncio.gather(
        client.start_loop(),
        requests()
    )

asyncio.run(main())
```

## Implemented methods

---

<b>The methods validate_token and get_charge_cards are stand-alone and to be used <u>before</u> connecting to the websocket with connect().</b>

<br>

#### await validate_token(api_token) -> bool

- Validates the given token.

#### await get_charge_cards(auth_token) -> list

- returns the users charge cards.

---

#### await connect(auth_token)

- Connects to the websocket.

#### set_receiver(receiver)

- Sets the receiver method.

#### await start_loop()

- Starts the receiver loop.

#### await wait_for_response()

- Waits until the next message is received.

#### await disconnect()

- Stops the connection.

<br>

### Data

---

#### await get_charge_points()

- Gets the chargepoints

#### await get_status(evse_id)

- Gets the status from a chargepoint.

#### await get_settings(evse_id)

- Gets the setting states from a chargepoint.

#### await get_grid_status(evse_id)

- Gets the grid status from a chargepoint.

<br>

### Settings

---

#### await set_public_charging(evse_id, value)

- Sets public charging to True or False.

#### await set_plug_and_charge(evse_id, value)

- Sets plug and charge to True or False.

#### await set_operative(evse_id, value)

- Sets operative to True or False.

<br>

### Actions

---

#### await reset(evse_id)

- Resets the chargepoint.

#### await reboot(evse_id)

- Reboots the chargepoint.

#### await start_session(evse_id card_uid)

- Starts a charge session.

#### await stop_session(evse_id)

- Stops a charge session.
