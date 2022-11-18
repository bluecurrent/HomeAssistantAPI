# Config Flow

## validate_input(client: Client, api_token: str)

- Validates the given api token.

## get_charge_cards(client: Client) -> list

- Returns the charge card related to the api token given to validate_input.

## ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN)

VERSION = 1

- input: dict[str, Any]
- cards: list
- client = Client()

### async_step_user(user_input: dict[str, Any] | None = None) -> FlowResult

- This method is called when a user adds the integration to Home Assistant. If the user_input is None it returns the form with `async_show_form`.
- If there is user input it checks if the token matches the current one
- If there is no match the token will get validated and the user's login / email is requested. If an exception happens it will add an error to the `errors` dict and this will be given to `async_show_form` and shown to the user.
- If there are no errors it sets the unique id and stores the current entry if there is one.
- If the user checked the `use your own charge card` box the card step will be started.
- If there is a current entry 'update_entry' is called and the flow will be aborted because the reauth is successful.
- Otherwise, the entry is created normally.

### async_step_card(user_input: dict[str, Any] | None = None) -> FlowResult

- This method works in the same way as `async_step_user`, only this time the api call to get the charge cards needs to happen before the user is shown the form.
- If `cards` is empty, the cards will be requested from the API, if an exception happens they are added to the `errors` dict in the same way as `async_step_user`.
- If there are no errors the card names get added to a `schema` and shown to the user.
- When this method gets called again with a selected card name, the uid will get added to `input`.
- If an entry already exists it will be updated with `update_entry`. Otherwise, a config entry is created.

### async_step_reauth async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult:

- Is called when the `ConfigEntryAuthFailed` exception is raised in `async_setup_entry` in `__init__.py`.
- Calls `async_step_user`.

### update_entry(self) -> None:

- Updates the existing entry and reload it.
