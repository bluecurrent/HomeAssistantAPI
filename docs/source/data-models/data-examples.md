# Response examples

## Data

### get_charge_points

```python
{
    'object': 'CHARGE_POINTS',
    'data': [
        {
            'evse_id': 'BCU100186',
            'name': '',
            'model_type': 'U:MOVE22',
            'chargepoint_type': 'UMOVE',
            'linked_charge_cards_only': False,
            'default_card': {
                'uid': 'BCU-APP',
                'id': 'BCU-APP',
                'name': '',
                'customer_name':
                'Samen Bluecurrent.nl'
            },
            'tariff': {
                'tariff_id': 'NLBCUT994',
                'price_ex_vat': 0.2397,
                'start_price_ex_vat': 0.0,
                'price_in_vat': 0.2613,
                'start_price_in_vat': 0.0,
                'currency': 'EUR',
                'permission': 'read'
            },
            'plug_and_charge_notification': False,
            'plug_and_charge': False,
            'publish_location': {
                'value': False,
                'permission': 'write'
            },
            'smart_charging': False,
            'activity': 'offline',
            'x_coord': 50.824811,
            'y_coord': 4.342838
        },
    ]
}
```

### await get_status(evse_id)

```python
{
    'object': 'CH_STATUS',
    'evse_id': 'BCU102728',
    'data': {
        'actual_p1': 0,
        'actual_p2': 0,
        'actual_p3': 0, 'activity':
        'available',
        'actual_v1': 0,
        'actual_v2': 0,
        'actual_v3': 0,
        'actual_kwh': 0,
        'max_usage': 10,
        'smartcharging_max_usage': 6,
        'max_offline': 7,
        'offline_since': None,
        'start_datetime': datetime.datetime(2022, 11, 10, 11, 41, 32, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>),
        'stop_datetime': datetime.datetime(2022, 11, 10, 11, 41, 50, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>),
        'total_cost': 0,
        'vehicle_status': 'standby',
        'evse_id': 'BCU102728',
        'avg_voltage': 0,
        'avg_current': 0,
        'current_left': 10,
        'total_kw': 0.0
    }
}
```

### await get_settings(evse_id)

```python
{
    "data": {
        "evse_id": "BCU102728",
        "plug_and_charge": False,
        "linked_charge_cards_only": False,
        "default_card": {
            "uid": "BCU-APP",
            "id": "BCU-APP",
            "name": "",
            "customer_name": "",
        },
        "smart_charging": True,
        "model_type": "U:MOVE22",
        "chargepoint_type": "UMOVE",
        "plug_and_charge_notification": False,
        "led_intensity": {"value": 0, "permission": "write"},
        "led_interaction": {"value": True, "permission": "write"},
    },
    "object": "CH_SETTINGS",
}
```

### await get_grid_status(evse_id)

```python
{
    "object": "GRID_STATUS",
    "data": {
        "id": "GRID-BCU102728",
        "grid_actual_p1": 0,
        "grid_actual_p2": 0,
        "grid_actual_p3": 0,
        "grid_max_install": 40,
        "grid_max_reserved": 25,
        "grid_avg_current": 0,
        "grid_max_current": 0,
    },
}
```

<br>

## Settings

### await set_linked_charge_cards_only(evse_id, value)

```python
{
    "object": "LINKED_CHARGE_CARDS_ONLY",
    "success": True,
    "flow_id": "",
    "evse_id": "BCU102728",
    "result": False,
    "error": "",
}
```

### await set_plug_and_charge(evse_id, value)

```python
{
    "object": "PLUG_AND_CHARGE",
    "success": True,
    "flow_id": "",
    "evse_id": "BCU102728",
    "result": False,
    "error": "",
}
```

### await block(evse_id, value)

- If the value changes, CH_STATUS is sent.

<br>

## Actions

### await reset(evse_id)

```python
{
    "object": "SOFT_RESET",
    "success": True,
    "flow_id": "",
    "evse_id": "BCU102728",
    "result": {},
    "error": "",
}
```

### await reboot(evse_id)

```python
{
    "object": "REBOOT",
    "success": True,
    "flow_id": "",
    "evse_id": "BCU102728",
    "result": {},
    "error": "",
}
```

### await start_session(evse_id, card_uid)

```python
{
    'object': 'START_SESSION',
    'success': True,
    'flow_id': '',
    'evse_id': 'BCU102728',
    'result': {},
    'error': ''
}
```

### await stop_session(evse_id)

```python
{
    'object': 'STOP_SESSION',
    'success': True,
    'flow_id': '',
    'error': ''
}
```
