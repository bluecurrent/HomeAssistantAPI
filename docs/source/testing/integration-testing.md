## Integration

### \_\_init\_\_.py

Contains the method `init_integration` which starts the BlueCurrent integration with a single platform (sensor, switch or button) and test data. Also, the whole bluecurrent api is patched here instead of in every test method.

### MockConfigEntry

MockConfigEntry is used to mock a config entry

### HomeAssistant

Most test methods have Home Assistant passed to them.

### states and entity registry

To check the state of an entity:

```python
 state = hass.states.get(f"button.{button}_101")
```

To get the entity

```python
 entity_registry.async_get(f"button.{button}_101")
```

### Platform tests

All platforms have two tests one to check if all entities are created and one if the value is updated.

### test_config_flow

The config flow needs to have 100% code coverage.

### Automation testing

The code could be made smaller but it works. And other integrations also have it like this.
