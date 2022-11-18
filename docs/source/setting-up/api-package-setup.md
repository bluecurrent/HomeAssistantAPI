# Setting up the API package

To get started developing the API package, you will have to install a few packages/programs. Depending on the
programming languages and tools you use, some configuration will be required.

## General requirements

to develop on the API package, the following tools are needed:

1. Python >= 3.8
2. python modules (no need to install these manually):
   - websockets
   - pyzt
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

### build documentation

- `make html`

### Using an updated API package (without publishing it).

1. `make build`
2. `pip install bluecurrent-api-<VERSION>-py3-none-any.whl`

### Using newer build of the API package in HA container (without publishing it).

1. Copy the `ha_package_installer_sample.bat` and rename it to `ha_package_installer.bat`.
   - If you are using Linux you can change the script to bash (keep the name ha_package_installer, so it will be ignored by git).
2. Change the variables:
   - container: the name of the HA devcontainer
   - version: the version of package
3. Run the script.

```{note}
bluecurrent_api-<VERSION>-py3-none-any.whl needs to match the .whl file in dist/ after make build
```
