# On_Data method

All relevant data that the API package receives will get routed to the `on_data` method.
This method then routes the message to the correct function based on the object_name of the data.

## CHARGE_POINTS

If the object name is `CHARGE_POINTS` the method `handle_charge_points` will be called. This method adds all evse_ids to the charge_points dict, sends status requests for all evse_ids and sends a grid status request.

## VALUE_TYPES

If the object name is `CHARGEPOINT_STATUS` or `CHARGEPOINT_SETTINGS` the key value pairs in the data will be added / updated in the charge_points dict for the evse_id. Then the `value_update` signal is dispatched with the evse_id.

## GRID_STATUS

If the object name is `GRID_STATUS` the data is stored in `grid` and the `grid_update_` signal is dispatched.

## SETTINGS

If the object name is `LINKED_CHARGE_CARDS_ONLY` or `PLUG_AND_CHARGE` the new state gets logged, updated in `charge_points` and the `value_update` signal is dispatched with the evse_id.

## SERVICES

If the object name is `SOFT_RESET`, `REBOOT`, `START_SESSION`, or `STOP_SESION` a success message or an error will be logged.
