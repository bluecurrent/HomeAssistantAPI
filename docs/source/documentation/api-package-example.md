# Api package example

To give a better view on how to package works here is an example on how to use the API package.

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
        await client.wait_for_response()
        await client.disconnect()

    # start the loop and send requests
    await asyncio.gather(
        client.start_loop(on_data),
        requests()
    )

asyncio.run(main())
```