# Integration

```
homeassistant/components/bluecurrent
 ┣ translations
 ┃ ┣ en.json
 ┃ ┣ nl.json
 ┃ ┣ sensor.en.json
 ┃ ┗ sensor.nl.json
 ┣ __init__.py
 ┣ button.py
 ┣ config_flow.py
 ┣ const.py
 ┣ device_condition.py
 ┣ device_trigger.py
 ┣ manifest.json
 ┣ sensor.py
 ┣ services.yaml
 ┣ strings.json
 ┣ strings.sensor.json
 ┗ switch.py

tests/components/bluecurrent
 ┣ __init__.py
 ┣ test_button.py
 ┣ test_config_flow.py
 ┣ test_device_condition.py
 ┣ test_device_trigger.py
 ┣ test_init.py
 ┣ test_sensor.py
 ┗ test_switch.py
```

## Code

### strings.json

Contains the strings for the config_flow that the user sees when adding the integration to Home Assistant.
`[%key:common]` means that it uses the string from `homeassistant/strings.json`. It also has the strings for the device_automations.

### strings.sensor.json

Contains the strings for the activity and vehicle status sensors.

### translations

Contains the strings for all languages.

### manifest.json

Defines information about the integration.

### services.json

Defines all services.

### const.py

Contains all the constants of the integration. All entities are defined here.

### sensor.py

Contains the setup and class for sensor platform.

### switch.py

Contains the setup and class for the switch platform.

### button

Contains the setup and class for the button platform.

### config_flow.py

Defines the setup flow of the integration. Contains two steps. One for the api token and the other for charge cards.

### \_\_init\_\_.py

Contains the setup method, the Connector Class that handles all incoming data from the api and the BlueCurrentEntity class that all the platforms inherit. It also adds device info to the entities and connects the dispatcher to listen for data updates.

## Tests

### \_\_init\_\_.py

Contains the method `init_integration` which starts the BlueCurrent integration with a single platform (sensor, switch or button) and test data.

### Other test files

The other test files contain tests for the file referenced in the name.
