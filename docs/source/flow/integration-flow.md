# Integration Flow

## Config Flow

The config flow gets started when a user adds the integration in Home Assistant.

The user will first see a field for their API token and a checkbox for if they would like to use a charge cards.

If the box is checked

PHOTOS

## Setup

After the config flow in completed the method `async_setup_entry` in \_\_init\_\_.py gets called by Home Assistant.
Here it retrieves the API token from the config_entry. And tries to connect to the API. If the connection is successful the `loop` gets started, then it waits until `CHARGE_POINTS` is received from the API and tells Home Assistant to start the platform setups with `async_setup_platforms`.

## on_data

All relevant data that the API package receives will get routed to the `on_data` method.
This method then routes the message to the correct function based on the object_name of the data.

[](on-data)

The variable `charge_points` in the Connector class holds the data of all the charge points.

## Platforms

In the platform files (sensor.py, switch.py, button.py) the method `async_setup_entry` will run, and the entities will be created for each charge point.
