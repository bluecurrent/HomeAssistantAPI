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


Hereby another example which works:

In order to run it from a Mac: install pip3
brew install pip3
pip3 install bluecurrent-api


my-venv/bin/python3 t.py

```python
from bluecurrent_api import Client
import asyncio


async def main():
    api_token = 'api_token'
    client = Client()

    # data receiver
    async def on_datax(data):
        print('received: ', data)

    async def on_open():
        print('open ws ')
#        await client.get_charge_cards()
#        await client.get_charge_points()

    # validate and set token.
    await client.validate_api_token(api_token)

    # example requests
    async def requests():
        await client.get_charge_cards()
        await client.get_charge_points()
        await asyncio.sleep(10)
        await client.disconnect()

    # connect and send requests
    await asyncio.gather(
        client.connect(on_datax,on_open),
        requests()
    )

asyncio.run(main())
```
