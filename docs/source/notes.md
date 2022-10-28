# Notes

## Keywords

### platform

the used base entities (sensor, switch, button)

```{note}
In the dev docs Home Assistant uses the word 'platform' for different things.
```

## Device Info

Device info is added to entities and not the other way around.

## Dummy Message
When the message `STATUS_START_SESSION` is received a dummy `CH_STATUS` message is send to the receiver method. This is because the value of start_datetime send with the next pushed `CH_STATUS` is the timestamp of the session before.

In Home Assistant the value of the start_datetime sensor is only updated when the new timestamp is newer than its value.

This does mean that the start_datetime value is not accurate but most of the time the difference is under 10 seconds.