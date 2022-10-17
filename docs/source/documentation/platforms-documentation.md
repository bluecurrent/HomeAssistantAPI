# Platforms

## BlueCurrentSensor(BlueCurrentEntity, SensorEntity)

\_attr_should_poll = False

### \_\_init\_\_(connector: Connector, sensor: SensorEntityDescription, evse_id: str | None = None)

- Passes the connector and the evse_id to BlueCurrentEntity.
- Sets the \_key, entity_description, unique_id and entity_id, and adds the evse_id to the last 2 if the entity is part of a charge point.

### update_from_latest_data()

- Is called when signal is dispatched.
- Gets the (potentially) new value from the connector class.
- If the value is not none, set the value and make the entity available.
- Else set the entity to unavailable except when the entity is one of `start_datetime` `stop_datetime` or `ch_offline_since`. Because those values are not always filled when receiving a status update.

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
