# API Package

```
HomeAssistantAPI
 ┣ src
 ┃ ┣ bluecurrent_api
 ┃ ┃ ┣ client.py
 ┃ ┃ ┣ exceptions.py
 ┃ ┃ ┣ py.typed
 ┃ ┃ ┣ utils.py
 ┃ ┃ ┣ websocket.py
 ┃ ┃ ┗ __init__.py
 ┣ tests
 ┃ ┣ test_client.py
 ┃ ┣ test_utils.py
 ┃ ┗ test_websocket.py
```

## Code

### \_\_init\_\_.py

Defines the module export.

### exceptions.py

Defines the exceptions used in the API package.

### py.typed
Marker file used to tell Mypy (type checker) that this package has type hints.

### client.py

Contains the Client class that has all the 'public' methods of the API package.

### websockets.py

Defines the Websocket Class that handles the connection to the Websocket.

### utils.py

Contains methods for modifying incoming data.