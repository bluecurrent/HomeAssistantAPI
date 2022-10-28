# Setting up Home Assistant

[HA docs](https://developers.home-assistant.io/docs/development_index/)

## Tasks

Home assistant has tasks that can be run inside Vscode:

Open command palette with `F1` or `ctrl+shift+p` and search for Tasks: run task

The important ones are:

- Run Home Assistant Core
- Generate requirements
- Install all requirements
- Install all test requirements

- pytest / pylint (Do not use these because they will run over the whole code)

## Installing

[Set up Development Environment](https://developers.home-assistant.io/docs/development_environment)

1. run task `Generate requirements`
2. run task `Install all requirements`

## Running

1. run task `Home Assistant Core`
2. go to [localhost:8123](http://localhost:8123)

## Testing

[Testing your code](https://developers.home-assistant.io/docs/development_testing)

1. run task `Install all Test Requirements`
2. `pytest tests/components/bluecurrent/`

### With coverage

- `pytest tests/components/bluecurrent/ --cov=homeassistant.components.<your_component> --cov-report term-missing -vv`

- Or run task `coverage` (integration can be specified)

## Lint

- pylint homeassistant/components/bluecurrent

## Submitting changes

[Submit your work](https://developers.home-assistant.io/docs/development_submitting)

[Development Checklist](https://developers.home-assistant.io/docs/development_checklist/)

- run task `generate all requirements`

- `python3 -m script.hassfest`

- `black --fast homeassistant tests`

## Rebasing

Follow [catching up with reality](https://developers.home-assistant.io/docs/development_catching_up)
