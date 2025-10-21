# Integration Flow

## Config Flow

The config flow gets started when a user adds the integration in Home Assistant from the integrations tab and entering their api token.


## Setup
After the config flow is completed the method `async_setup_entry` in \_\_init\_\_.py gets called by Home Assistant.
Here it retrieves the API token from the config_entry. And validates it. If the validation is successful a background task to connect and listen to the websocket is started, then the function waits until `CHARGE_POINTS` is received from the API and tells Home Assistant to start the platform setups with `async_setup_platforms`.

## Platforms

In the platform classes (sensor.py, switch.py, button.py) the method `async_setup_entry` will run, and the entities will be created for each charge point.

## on_data

All relevant data that the API package receives will get routed to the `on_data` method.
This method then routes the message to the correct function based on the object_name of the data.

[](on-data)

The variable `charge_points` in the Connector class holds the data of all the charge points.

## Platform update

All charge point entities listen to the `bluecurrent_value_update_<evse_id>`event and grid entities listen to `bluecurrent_grid_update`. When the event is dispatched the entity checks if its value in the`charge_points` dict in the Connector class is not none. If that is the case the value will be updated in the entity. Otherwise, the entity will be set unavailable.

```{note}
With timestamps the value will not be set to unavailable because the API will not send the timestamp every time.
```
