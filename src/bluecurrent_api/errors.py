class BlueCurrentError(Exception):
    """Define a base error."""

    pass


class WebsocketError(BlueCurrentError):
    """Define an error related to the connection."""

    pass


class InvalidToken(BlueCurrentError):
    """Define an error related to invalid tokens."""
    pass


class NoCardsFound(BlueCurrentError):
    """Define an error for when a token has no cards."""
    pass
