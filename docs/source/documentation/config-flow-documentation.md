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
- If there is user input a unique id is created for the integration instance and if this id already exists the config flow is aborted.
- If the id doesn't already exist the api token will get validated. If an exception happens it will add an error to the `errors` dict and this will be given to `async_show_form` and shown to the user.
- If there are no errors the config entry will be created with `BCU_APP` as charge_card uid or if the user checked the `use your own charge card` box the card step will be started.

### async_step_card(user_input: dict[str, Any] | None = None) -> FlowResult

- This method works in the same way as `async_step_user`, only this time the api call to get the charge cards needs to happen before the user is shown the form.
- If `cards` is empty, the cards will be requested from the API, if an exception happens they are added to the `errors` dict in the same way as `async_step_user`.
- If there are no errors the card names get added to a `schema` and shown to the user.
- When this method gets called again with a selected card name, the uid will get added to `input` and a config entry is created.
