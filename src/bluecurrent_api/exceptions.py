"""Define package errors."""


class BlueCurrentException(Exception):
    """Define a base error."""


class WebsocketException(BlueCurrentException):
    """Define an error related to the websocket connection."""


class RequestLimitReached(BlueCurrentException):
    """Define an error for when the request limit is reached."""


class InvalidApiToken(BlueCurrentException):
    """Define an error related to an invalid token."""


class NoCardsFound(BlueCurrentException):
    """Define an error for when a token has no cards."""
