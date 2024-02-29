# Notes

## Keywords

### platform

the used base entities (sensor, switch, button)

```{note}
In the dev docs Home Assistant uses the word 'platform' for different things.
```

## Device Info

Device info is added to entities and not the other way around.

## Error handling

If something goes wrong server side an `ERROR` object is sent and an `WebsocketError` is raised in the api package. Setting and Action request can also have an error in their `RECEIVED_` or `STATUS_` messages, but this is sent to HA and logged.

## API and AUTH token

To use this the api package the user first validates his api token with `VALIDATE_API_TOKEN` (token can be generated in my.bluecurrent.nl -> advanced -> home assistant api token). If the token is used, the auth token is returned and stored in `auth_token` in `websocket.py` all other requests add this token for authentication.
