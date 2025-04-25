# Response examples

## Data

### description

# CHARGE_POINTS

### General Fields

| Field                        | Type    | Description                                                                      | Example                     |
|------------------------------|---------|----------------------------------------------------------------------------------|-----------------------------|
| `evse_id`                     | String  | Identifier of the charge point                                                   | `BCU100186`                 |
| `name`                        | String  | Name given by the owner                                                          | `My Charge Point`           |
| `model_type`                  | String  | Model name of the charge point                                                   | `U:MOVE22`                  |
| `chargepoint_type`            | String  | Type name of the charge point                                                    | `UMOVE`                     |
| `activity`                    | String  | Status of the charge point (`available`, `charging`, `offline`, `error`)         |                             |
| `x_coord`                     | Float   | GPS x-coordinate                                                                  | `50.824811`                 |
| `y_coord`                     | Float   | GPS y-coordinate                                                                  | `4.342838`                  |
| `linked_charge_cards_only`    | Boolean | Only linked cards can charge here (`True`) or all public cards allowed (`False`) |                             |
| `plug_and_charge_notification`| Boolean | Send push notification to the app when the charge point starts charging with plug-and-charge enabled |                             |
| `plug_and_charge`             | Boolean | Start charging when the cable is inserted, or requires a card first              |                             |
| `smart_charging`              | Boolean | Whether smart charging is enabled                                                |                             |

### Card

| Field                        | Type    | Description                                                   | Example                        |
|------------------------------|---------|---------------------------------------------------------------|--------------------------------|
| `default_card.uid`            | String  | Internal card number used for transactions                    | `046C8CCA8C1D90`               |
| `default_card.id`             | String  | Visual card number                                            | `NL-ANW-CZPYJFFML-3`           |
| `default_card.name`           | String  | Name given to the card by the owner                           | `My Charge Card`              |
| `default_card.customer_name`  | String  | Owner's name                                                   | `BlueCurrent Together`         |

### Tariff

| Field                        | Type    | Description                                                   | Example      |
|------------------------------|---------|---------------------------------------------------------------|--------------|
| `tariff.tariff_id`            | String  | Tariff ID shared with card providers                          | `NLBCUT994`  |
| `tariff.price_ex_vat`         | Float   | Price per kW excluding VAT                                    | `0.2347`     |
| `tariff.start_price_ex_vat`   | Float   | Start fee excluding VAT for a transaction                     | `1.50`       |
| `tariff.price_in_vat`         | Float   | Price per kW including VAT                                    | `0.2613`     |
| `tariff.start_price_in_vat`   | Float   | Start fee including VAT for a transaction                     | `1.815`      |
| `tariff.currency`             | String  | Currency for the tariff                                       | `EUR`        |
| `tariff.permission`           | String  | Permission to view/edit the tariff (`read`, `write`, etc.)    | `read`       |

### Publishing

| Field                        | Type    | Description                                                   |
|------------------------------|---------|---------------------------------------------------------------|
| `publish_location.value`     | Boolean | Is the charge point published on external sites               |
| `publish_location.permission`| String  | Permission to publish the location (`write`, etc.)            |

---

# CH_STATUS

| Field                       | Type    | Description                                                             |
|-----------------------------|---------|-------------------------------------------------------------------------|
| `actual_p1`, `actual_p2`, `actual_p3` | Integer | Current (Amps) being drawn on phase 1/2/3                               |
| `activity`                  | String  | Status (`available`, `charging`, `offline`, `error`)                    |
| `actual_v1`, `actual_v2`, `actual_v3` | Float   | Voltage on phase 1/2/3                                                  |
| `actual_kwh`                | Float   | kWh charged since the start of the transaction                          |
| `max_usage`                 | Integer | Maximum current allowed per phase                                       |
| `smartcharging_max_usage`   | Integer | Max current allowed by smart charging per phase                        |
| `max_offline`               | Integer | Amps used when offline                                                  |
| `offline_since`             | String  | Timestamp when the charger went offline                                |
| `start_datetime`            | String  | Start/stop time of last transaction (currently disabled)               |
| `total_cost`                | Float   | Total cost of last transaction in euros (currently disabled)           |
| `vehicle_status`            | String  | Status of the vehicle (`A`, `B`, `C`, or `ready`, `charging`)           |
| `evse_id`                   | String  | Identifier of the charge point                                         |
| `avg_voltage`               | Float   | Average voltage over 3 phases                                          |
| `avg_current`               | Integer | Average current on phase 1 (or total?)                                 |

---

# CH_SETTINGS

| Field                         | Type    | Description                                                    |
|-------------------------------|---------|----------------------------------------------------------------|
| `evse_id`                     | String  | Identifier of the charge point                                 |
| `model_type`                  | String  | Model name of the charge point                                 |
| `chargepoint_type`            | String  | Type name of the charge point                                  |
| `plug_and_charge`             | Boolean | Whether the charger starts automatically                       |
| `linked_charge_cards_only`    | Boolean | Only allow linked cards                                        |
| `smart_charging`              | Boolean | Is smart charging enabled                                      |
| `plug_and_charge_notification`| Boolean | Notify via app when plug-and-charge activates                 |

### LED Settings

| Field                        | Type    | Description                                                       |
|------------------------------|---------|-------------------------------------------------------------------|
| `led_intensity.value`        | Integer | Intensity of the LEDs                                             |
| `led_intensity.permission`   | String  | Permission to modify LED intensity                                |
| `led_interaction.value`      | Boolean | Enable/disable LED interaction (lights only on action)            |
| `led_interaction.permission` | String  | Permission to modify LED interaction                              |

### Card Info

(Same structure as in CHARGE_POINTS)

---

# GRID_CURRENT

| Field              | Type    | Description                                         |
|--------------------|---------|-----------------------------------------------------|
| `evse_id`          | String  | Identifier of the charge point                      |
| `grid_actual_p1`   | Integer | Building load on phase 1                            |
| `grid_actual_p2`   | Integer | Building load on phase 2                            |
| `grid_actual_p3`   | Integer | Building load on phase 3                            |

### get_charge_points

```bash
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

```bash
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

```bash
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

```bash
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

```bash
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

```bash
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

```bash
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

```bash
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

```bash
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

```bash
{
    'object': 'STOP_SESSION',
    'success': True,
    'flow_id': '',
    'error': ''
}
```
