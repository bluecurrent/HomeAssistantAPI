# Data flow

## Integration

All incomming websocket messages are send to the on_data method inside the Connector class in `__init__.py`.'

Inside this method the message is routed based on the object_name.

If the message contains data for a charge point it gets added to the charge_point dict in Connector and a signal is send with the evse_id. The entities of that charge point are listening to this and will change their value.
