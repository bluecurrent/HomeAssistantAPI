# Platform update

All charge*point entities listen to the `bluecurrent_value_update*<evse_id>`event. When the event is dispatched the entity checks if its state is not null in the`charge_points` dict in the Connector class. If that is the case the value will be updated in the entity. Otherwise, the entity will be set unavailable.

With timestamps the value will not be set to unavailable because the API will not send the timestamp every time.
