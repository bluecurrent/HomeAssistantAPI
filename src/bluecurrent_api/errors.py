class BlueCurrentError(Exception):
    """Define a base error."""


class WebsocketError(BlueCurrentError):
    """Define an error related to the connection."""


class InvalidToken(BlueCurrentError):
    """Define an error related to an invalid token"""


class NoCardsFound(BlueCurrentError):
    """Define an error for when a token has no cards."""
