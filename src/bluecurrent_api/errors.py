class BlueCurrentError(Exception):
    """Define a base error."""

    pass


class WebsocketError(BlueCurrentError):
    """Define an error related to the connection."""

    pass


class InvalidToken(BlueCurrentError):
    """Define an error related to invalid tokens."""
    pass