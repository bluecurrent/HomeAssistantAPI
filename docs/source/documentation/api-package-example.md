# Api package example

To give a better view on how to package works here is an example on how to use the API package.


```python
from bluecurrent_api import Client
import asyncio


async def main():
    api_token = 'api_token'
    client = Client()

    # data receiver
    async def on_data(data):
        print('received: ', data)

    # validate and set token.
    await client.validate_api_token(api_token)

    # example requests
    async def on_open():
        await client.get_charge_points()
        await asyncio.sleep(10)
        await client.disconnect()

    # connect and send requests
    await client.connect(on_data, on_open)

asyncio.run(main())
```

In order to run it from a Mac: install pip3
brew install pip3
pip3 install bluecurrent-api


my-venv/bin/python3 t.py
