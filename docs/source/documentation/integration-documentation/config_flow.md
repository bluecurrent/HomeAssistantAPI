# ConfigFlow

```{eval-rst}
.. automodule:: homeassistant.components.blue_current.config_flow
   :members:
   :private-members:
   :special-members:
   :exclude-members: __weakref__
```

### async_step_user
- This method is called when a user adds the integration to Home Assistant. If the user_input is None it returns the form with `async_show_form`.
- If there is user input it will validate the given token and get the customer id and email. The customer id is used as the unique id of the config entry and the email as title.
- If an exception happens it will add an error to the `errors` dict and this will be given to `async_show_form` and shown to the user.
- If there are no errors it sets the unique id and stores the current entry if there is one.
- If there is a current entry 'update_entry' is called and the flow will be aborted because the reauth is successful.
- Otherwise, the entry is created normally.


### async_step_reauth

- Is called when a config is reconfigured. This button is shown when the `ConfigEntryAuthFailed` exception is raised in `async_setup_entry` in `__init__.py`.
- Calls `async_step_user` in which the entry is updated instead of creating a new one.