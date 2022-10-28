# API Package

```
HomeAssistantAPI
 ┣ src
 ┃ ┣ bluecurrent_api
 ┃ ┃ ┣ client.py
 ┃ ┃ ┣ exceptions.py
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

### client.py

Contains the Client class that has all the 'public' methods of the API package.

### websockets.py

Defines the Websocket Class that handles the connection to the Websocket.

### utils.py

Contains methods for modifying incoming data.

## Tests

The test files contain tests for the file referenced in the name.

See [](../testing/api-package-testing.md)
