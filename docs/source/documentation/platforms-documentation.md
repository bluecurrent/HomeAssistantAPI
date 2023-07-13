# Platforms

## ChargePointSensor(BlueCurrentEntity, SensorEntity)

\_attr_should_poll = False

### \_\_init\_\_(connector: Connector, sensor: SensorEntityDescription, evse_id: str)

- Passes the connector and the evse_id to BlueCurrentEntity.

### update_from_latest_data()

- Is called when signal is dispatched.
- Gets the (potentially) new value from the connector class.
- If the value is not none, set the value and make the entity available. But if the entity is a timestamp entity (start_datetime, stop_datetime, offline_since) and the sensor value is not None or the new value is older than don't update the value.
- Else set the entity to unavailable except when the entity is a timestamp entity.

See [](../notes.md)

## GridSensor(SensorEntity)

\_attr_should_poll = False

### \_\_init\_\_(connector: Connector, sensor: SensorEntityDescription)

- Initializes a grid sensor.

### async_added_to_hass(self)
- Connects the dispatcher to a signal to call `update` when triggered.
Update method calls `update_from_latest_data()` and writes the state to HA.

### update_from_latest_data()
- Updates the sensor value.
- If the value is None, it sets the sensor to unavailable.

## ChargePointButton(BlueCurrentEntity, ButtonEntity):

\_attr_should_poll = False

### \_\_init\_\_(connector: Connector, evse_id: str, button: ButtonEntityDescription)

- Passes the connector and the evse_id to BlueCurrentEntity.
- Sets the \_service, entity_description, unique_id and entity_id.

### async_press()

- Called when the button is pressed.
- Calls its service with an evse_id.

### update_from_latest_data()

- Not implemented.

## ChargePointSwitch(BlueCurrentEntity, SwitchEntity)

\_attr_should_poll = False

### \_\_init\_\_(connector: Connector, evse_id: str, switch: dict[str, Any])

- This function differs from the other ones because of \_function it couldn't use SwitchEntityDescription.
- But it does the same as the `self.entity_description = ` only manually.

### call_function(value: bool)

- Calls the function to send the request to the API with the given value. Logs an error if there is no connection with the API.

### async_turn_on()

- Turns the setting on.

### async_turn_off()

- Turns the setting off

### update_from_latest_data()

- Is called when signal is dispatched.
- Gets the (potentially) new value from the connector class.
- If the value is not none, set the value and make the entity available.
- Else set the entity to unavailable.
