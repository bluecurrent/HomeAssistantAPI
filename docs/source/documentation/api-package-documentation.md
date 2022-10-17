# API Package

## Example implementation

To give a better view on how to package works here is an example on how to use the API package.

First an instance of the client is created. Then a receiver is given to the `set_receiver` method. All incoming messages will be routed to the given method.

Then connect to the API is made with `connect` with an API token generated in the driver portal.

And last with `asyncio.gather` the loop is started, and the requests will be sent.

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
        await client.disconnect()

    # start the loop and send requests
    await asyncio.gather(
        client.start_loop(),
        requests()
    )

asyncio.run(main())
```

## Client

The Client class has all the 'public' methods of the package.

### await validate_token(api_token) -> bool

- Validates the given token.

### await get_charge_cards(auth_token) -> list

- Returns the users charge cards.

<b>The methods validate_token and get_charge_cards are stand-alone and to be used <u>before</u> connecting to the websocket with connect().</b>

---

### await connect(auth_token)

- Connects to the websocket.

### set_receiver(receiver)

- Sets the receiver method.

### await start_loop()

- Starts the receiver loop.

### await wait_for_response()

- Waits until the next message is received.

Only really used for waiting to start the Home Assistant setup until `CHARGE_POINTS` is received but could be extended for other things.

### await disconnect()

- Stops the connection.

<br>

### Data

#### await get_charge_points()

- Gets the charge points

#### await get_status(evse_id)

- Gets the status from a charge point.

#### await get_settings(evse_id)

- Gets the setting states from a charge point.

#### await get_grid_status(evse_id)

- Gets the grid status from a charge point.

<br>

### Settings

#### await set_public_charging(evse_id, value)

- Sets public charging to True or False.

#### await set_plug_and_charge(evse_id, value)

- Sets plug and charge to True or False.

#### await set_operative(evse_id, value)

- Sets operative to True or False.

The `set_operative' setting request is different from the other to setting requests in that it has different commands instead of a boolean for changing the state.

<br>

### Actions

#### await reset(evse_id)

- Resets the charge point.

#### await reboot(evse_id)

- Reboots the charge point.

#### await start_session(evse_id, card_uid)

- Starts a charge session.

#### await stop_session(evse_id)

- Stops a charge session.

The `stop_session` request uses `evseid` instead of `evse_id` in the request.

---

### \_create_request(self, command, evse_id=None, value=None, card_uid=None) -> dict

The Client class also has a 'private' method that returns a dictonary with the correct key, value pair for each request.

## Websocket

The Websocket class does all the work of sending and receiving messages.

### get_receiver_event() -> asyncio.Event

- Returns cleared receive_event when connected.

### validate_api_token(api_token) -> bool

- Returns True when the token is correct or throws an InvalidApiToken error.

- Stores the received `auth_token` in the Websocket class.

### get_charge_cards() -> list

- Returns the charge cards or an NoCardsFound exception.

Also throws WebsocketException if `auth_token` is not set with `validate_api_token`.

### set_receiver(self, receiver: Callable)

- Sets the receiver and if the receiver asynchronous or not.

### connect(api_token)

- Validates the given api_token and calls `_connect`.

If there already is a connection an WebsocketException is thrown.

### \_connect()

Tries to connect to websocket and stores the connection in a variable. Also sets \_has_connection to True.

Throws WebsocketException if connecting has failed.

### send_request(request: dict)

Checks if the receiver and auth_token are set and throws WebsocketException if not.

Adds `Authorization` to request dict and calls `_send`.

### loop()

Trows error if the receiver is not set.

Sends `HELLO` command to API so that the API will send messages back if status changes.

Creates an infinite loop that calls `_message_handler` and stops if \_message_handler throws an error or returns True.

### \_message_handler()

- Handles all incoming messages from `_recv`.

Awaits the next message with `_recv`.

If the websocket has disconnected and `_recv` returns None return True to so that the loop is stopped in `loop`.

Throws WebsocketException if object_name is None.

Ignore messages with "RECEIVED" in object_name and no error and HELLO.

Throws WebsocketException if message has an error code.

Call util methods based on object_name.

Plug_and_charge and public_charging status get handled by handle_setting_change.

Operative is ignored because if it is successful ch_status will also be received.

Calls `handle_receive_event` to set the event.

Pass the message to the receiver method.

### \_send(data: dict)

- Sends data to the websocket.
  Checks connection with `_check_connection`

Tries to send a JSON message to websocket and calls `handle_connection_errors()` on errors.

### \_recv() -> dict

- Receives data from the websocket.

Checks connection with `_check_connection`.

Tries to send JSON message to websocket and calls `handle_connection_errors()` on errors.

### handle_connection_errors()

- Handles connection errors.

If `_has_connection` is still True set it to false, calls `handle_receive_event` to unblock. And throw an WebsocketException.

### disconnect()

- Closes the connection

Throws an WebsocketException if \_has_connection is already False.

Calls `handle_receive_event` to unblock.

### \_check_connection()

Throws an WebsocketException if connection is None.

### handle_receive_event():

- Sets receive_event if it exists.

## Utils

Contains methods for modifying incoming data.

### calculate_average_usage_from_phases(phases tuple) -> float

- Returns the average of used phases.

### calculate_total_kw(current: tuple, v_avg) -> float

- Returns an estimate of the total kw.

### create_datetime(timestamp: str) -> datetime

- Returns a timestamp.

Adds CEST timezone if not already in timestamp.

### get_vehicle_status(vehicle_status_key: str) -> str

- Returns the vehicle status.

### handle_status(message: dict)

- Transforms key, value pairs to the given messages and modifies others.

### handle_grid(message: dict)

- Adds total and avg grid current to given message.

### handle_setting_change(message: dict)

- Change the result to a boolean and modifies the object.

### handle_session_messages(message: dict)

- Changes the object name.

Changes the error to a better readable form.
