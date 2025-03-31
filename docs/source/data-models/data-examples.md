# Response examples

## Data

### description

object CHARGE_POINTS
====================
Generieke velden:
evse_id                       String:   De identifier van het laadpunt                    -- bijvoorbeeld BCU100186
name                          String:   De naam zoals de eigenaar eraan gegeven heeft     -- bijvoorbeeld Mijn Laadpunt  
model_type                    String:   De model naam van het laadpunt                    -- bijvoorveeld U:MOVE22
chargepoint_type              String:   De type naam van het laadpunt                     -- bijvoorbeeld UMOVE
activity                      String:   Status van het laadpunt (available, charging, offline, error)
x_coord                       Float:    GPS x-coordinaat van het laadpunt                 -- bijvoorbeeld 50.824811
y_coord                       Float:    GPS y-coordinaat van het laadpunt                 -- bijvoorbeeld 4.342838
linked_charge_cards_only      Boolean:  Mag hier alleen maar met toegevoegde passen geladen worden (True) of met alle publieke passen (False)
plug_and_charge_notification  Boolean:  Wordt er een pushnotificatie naar de mobile app gestuurd als het laadpunt start met laden als plug en charge aanstaat?
plug_and_charge               Boolean:  Start het laadpunt zodra er een kabel ingestoken wordt, of moet er eerst een pas voor gehouden worden?
smart_charging                Boolean:  Wordt er gebruik gemaakt van slim laden

Pas:
default_card.uid              String:   Het interne pasnummer van de pas die default voor transacties gebruikt wordt  -- bijvoorbeeld: 046C8CCA8C1D90
default_card.id               String:   Het visuele pasnummer van de pas die default voor transacties gebruikt wordt  -- bijvoorbeeld: NL-ANW-CZPYJFFML-3
default_card.name             String:   De naam die de eigenaar aan de pas gegeven heeft                              -- bijvoorbeeld: Mijn laadpas
default_card.customer_name    String:   De naam van de eigenaar                                                       -- Bijvoorbeeld: Samen BlueCurrent

Tarief:
tariff.tariff_id              String:   Het tariefID zoals dit wordt gedeeld met pasleveranciers  -- bijvoorbeeld NLBCUT994
tariff.price_ex_vat           Float:    Het tarief exclusief BTW per kW                           -- bijvoorbeeld 0.2347
tariff.start_price_ex_vat     Float:    Het start tarief exclusief BTW voor 1 transactie          -- bijvoorbeeld 1.50
tariff.price_in_vat           Float:    Het tarief inclusief BTW per kW                           -- bijvoorbeeld 0.2613
tariff.start_price_in_vat     Float:    Het start tarief inclusief BTW voor 1 transactie          -- bijvoorbeeld 1.815
tariff.currency               String:   De valuta voor het tarief                                 -- bijvoorbeeld EUR
tariff.permission             String:   Mag de gebruiker het tarief inzien en/of wijzigen         -- bijvoorbeeld read

Publiceren:
publish_location.value        Boolean:  Is het laadpunt gepubliceerd op externe sites  
publish_location.permission   String:   Mag de gebruiker het laadpunt publiceren                  -- bijvoorbeeld write (ja)


Object CH_STATUS
================
actual_p1                 Integer:  Hoeveel ampere wordt er op dit moment op fase 1 geladen?
actual_p2                 Integer:  Hoeveel ampere wordt er op dit moment op fase 2 geladen?
actual_p3                 Integer:  Hoeveel ampere wordt er op dit moment op fase 3 geladen?
activity                  String:   Status van het laadpunt (available, charging, offline, error)
actual_v1                 Float:    Hoeveel spanning staat er op dit moment op fase 1?
actual_v2                 Float:    Hoeveel spanning staat er op dit moment op fase 2?
actual_v3                 Float:    Hoeveel spanning staat er op dit moment op fase 3?
actual_kwh                Float:    Hoeveel kWh is er op dit moment, sinds de start van de transactie, geladen?
max_usage                 Integer:  Hoeveel ampere mag er maximaal geladen worden (per fase)?
smartcharging_max_usage   Integer:  Hoeveel ampere mag het smart charging algoritme maximaal geven aan het laadpunt (per fase)?  
max_offline               Integer:  Met hoeveel ampere wordt er geladen als het laadpunt geen verbinding heeft met de backoffice?  
offline_since             String:   Indien offline, sinds wanneer is het laadpunt offline?
start_datetime            String:   Tijdstip waarop de laatste transactie gestart is. Deze staat op dit moment uit.
start_datetime            String:   Tijdstip waarop de laatste transactie gestopt is. Deze staat op dit moment uit.
total_cost                Float:    De totale kosten in Euro van de laatste transactie. Deze staat op dit moment uit.
vehicle_status            String:   Status van de auto. (A, B or C of ready/charging)
evse_id                   String:   De identifier van het laadpunt                   
avg_voltage               Float:    Gemiddelde spanning van de drie fases op dit moment.  
avg_current               Integer:  Hoeveel ampere wordt er op dit moment op fase 1 geladen?

Object CH_SETTINGS
==================
evse_id                       String:   De identifier van het laadpunt                    -- bijvoorbeeld BCU100186
model_type                    String:   De model naam van het laadpunt                    -- bijvoorveeld U:MOVE22
chargepoint_type              String:   De type naam van het laadpunt                     -- bijvoorbeeld UMOVE
plug_and_charge               Boolean:  Start het laadpunt zodra er een kabel ingestoken wordt, of moet er eerst een pas voor gehouden worden?
linked_charge_cards_only      Boolean:  Mag hier alleen maar met toegevoegde passen geladen worden (True) of met alle publieke passen (False)
smart_charging                Boolean:  Wordt er gebruik gemaakt van slim laden
plug_and_charge_notification  Boolean:  Wordt er een pushnotificatie naar de mobile app gestuurd als het laadpunt start met laden als plug en charge aanstaat?

Led:
led_intensity.value           Integer  Intensiteit van de leds
led_intensity.permission      String:   Mag de gebruiker de led intensiteit aanpassen
led_interaction.value         Boolean:  Kan de interactie van de leds aan of uit. Leds gaan dan alleen branden al je een actie uitvoert
led_interaction.permission    String:   Mag de gebruiker de led interactie aanpassen

Pas:
default_card.uid              String:   Het interne pasnummer van de pas die default voor transacties gebruikt wordt  -- bijvoorbeeld: 046C8CCA8C1D90
default_card.id               String:   Het visuele pasnummer van de pas die default voor transacties gebruikt wordt  -- bijvoorbeeld: NL-ANW-CZPYJFFML-3
default_card.name             String:   De naam die de eigenaar aan de pas gegeven heeft                              -- bijvoorbeeld: Mijn laadpas
default_card.customer_name    String:   De naam van de eigenaar                                                       -- Bijvoorbeeld: Samen BlueCurrent

Object GRID_CURRENT
===================
evse_id                       String:   De identifier van het laadpunt                    -- bijvoorbeeld BCU100186
grid_actual_p1                Integer:  Hoeveel ampere wordt er op dit moment op fase 1 verbruikt in het gebouw?
grid_actual_p2                Integer:  Hoeveel ampere wordt er op dit moment op fase 2 verbruikt in het gebouw?
grid_actual_p3                Integer:  Hoeveel ampere wordt er op dit moment op fase 3 verbruikt in het gebouw?



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
