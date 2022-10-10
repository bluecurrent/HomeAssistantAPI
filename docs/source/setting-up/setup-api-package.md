# Setting up the api package

To get started developing the api package, you will have to install a few packages/programs. Depending on the
programming languages and tools you use, some configuration will be required.

## General requirements

to develop on the api package, the following tools are needed:

1. Python >= 3.8
2. python modules (no need to install these manually):
   - websockets
   - pylint
   - pytest
   - pytest-mock
   - pytest-cov
   - pytest-asyncio
   - coverage

## Make commands

### installing

1. `git clone https://github.com/bluecurrent/HomeAssistantAPI.git`
2. `make install`

### testing

- `make test`
- `make lint`

### publishing

1. `make build`
2. `make publish`

### using updated api package

1. `make build`
2. `pip install bluecurrent_api-<VERSION>-py3-none-any.whl`

### using newer build of the api in HA container.

If you want to use a newer build of the api package in the Home Assistant container.

`make build`

`docker cp dist\bluecurrent_api-<VERSION>-py3-none-any.whl <CONTAINER>:/workspaces/core/`

`docker exec <CONTAINER> pip install core/bluecurrent_api-<VERSION>-py3-none-any.whl --no-deps --force-reinstall`

`docker exec <CONTAINER> rm core/bluecurrent_api-<VERSION>-py3-none-any.whl`

packagemanager.bat
