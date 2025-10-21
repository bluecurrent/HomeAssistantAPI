# Notes

## Keywords

### platform

the used base entities (sensor, switch, button)

```{note}
In the dev docs Home Assistant uses the word 'platform' for different things.
```

## Device Info

Device info is added to entities and not the other way around.

## Device ID

In Home Assistant, each device is assigned a unique device ID that acts as its identifier within the system. The device ID itself is managed internally by Home Assistant and is stable across restarts.

## Error handling

If something goes wrong server side an `ERROR` object is sent and an `WebsocketError` is raised in the api package. Setting and Action request can also have an error in their `RECEIVED_` or `STATUS_` messages, but this is sent to HA and logged.

## API and AUTH token

To use this the api package the user first validates his api token with `VALIDATE_API_TOKEN` (token can be generated in my.bluecurrent.nl -> advanced -> home assistant api token). If the token is used, the auth token is returned and stored in `auth_token` in `websocket.py` all other requests add this token for authentication.

## HA-Bluecurrent and official integration
As of 2024 bluecurrent has been added to Home Assistant. [link](https://www.home-assistant.io/integrations/blue_current/). This version currently only has the sensors and cannot start a session for example. 

It has changed quite compared to ha-bluecurrent. the idea is deprecate ha-bluecurrent after a session can be started. 

One of the many changes is that a start session will become a select instead of a button so that the charge card can be selected when starting the session instead of at the installation of the integration.