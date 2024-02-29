# Setting up the API package

## General requirements

to develop on the API package, the following tools are needed:

1. Python >= 3.11
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

```{note}
Make commands can be used on Windows with GnuWin or just running the commands defined in the make file.
```

### installing

1. `git clone https://github.com/bluecurrent/HomeAssistantAPI.git`
2. `python -m venv venv`
3. `make install`

### testing

- `make test`
- `make test-cov`

### lint, format, typechecking
- `make lint`
- `make ruff`
- `make black`
- `make mypy`

### publishing

1. `make build`
2. `make publish` (credentials stored in password manager)

### build documentation

- `make html`

### Using an updated API package (without publishing it).

1. `make build`
2. `pip install bluecurrent-api-<VERSION>-py3-none-any.whl`

### Using newer build of the API package in a HA dev container (without publishing it).

1. move the .whl file to the container with `docker cp dist/bluecurrent-api-<VERSION>-py3-none-any.whl`
2. install the package inside the container
3. remove the .whl file.

### Publish checklist
1. Run tests, lint, format and type checker.
2. Increment version in pyproject.toml.
3. make build
4. For large changes install new package in Ha container and run integration tests and start ha and test manually.
5. Push to git
6. Wait until checks are successful.
7. make publish



