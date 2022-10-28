# Automations

[device automations](https://developers.home-assistant.io/docs/device_automation_index)

## Triggers

First the types are stored in the TYPES constants, Then trigger schemas are defined and stored in a tuple.

### async_get_triggers(hass: HomeAssistant, device_id: str) -> list[dict[str, Any]]

- Is called when opening the trigger dropdown of a charge point.
- Returns all triggers of a charge point.

### async_attach_trigger(hass: HomeAssistant, config: ConfigType, action: TriggerActionType, trigger_info: TriggerInfo) -> CALLBACK_TYPE:

- Is called when creating an automation with a charge point trigger in HA.

## Conditions

First the types are stored in the TYPES constants, Then trigger schemas are defined and stored in a tuple.

### async_get_conditions(hass: HomeAssistant, device_id: str) -> list[dict[str, Any]]

- Is called when opening the condition dropdown of a charge point.
- Returns all conditions of a charge point.

### async_condition_from_config(hass: HomeAssistant, config: ConfigType) -> condition.ConditionCheckerType:

- Is called when creating an automation with a charge point condition in HA.
