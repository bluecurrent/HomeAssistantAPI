# Api package example

To give a better view on how to package works here is an example on how to use the API package.

First an instance of the client is created.

Then connection with the API is made with `connect` with an API token generated in the driver portal.

And last with `asyncio.gather` the loop is started, and a receiver is given. All incoming messages will be routed to the given method.

```python
from bluecurrent_api import Client
import asyncio


async def main():
    api_token = 'api_token'
    client = Client()

    # data receiver
    def on_data(data):
        print('received: ', data)

    # connect to the websocket
    await client.connect(api_token)

    # example requests
    async def requests():
        await client.get_charge_points()
        await client.disconnect()

    # start the loop and send requests
    await asyncio.gather(
        client.start_loop(on_data),
        requests()
    )

asyncio.run(main())
```