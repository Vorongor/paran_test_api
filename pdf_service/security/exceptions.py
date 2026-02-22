class TokenExpiredError(Exception):
    """Raised when a token is expired."""

    pass


class InvalidTokenError(Exception):
    """Raised when a token is invalid."""

    pass
