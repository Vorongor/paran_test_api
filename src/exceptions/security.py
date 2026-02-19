class BaseSecurityException(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Something went wrong during account operation"
        super().__init__(message)


class TokenExpiredError(BaseSecurityException):
    """Exception raised when a token is expired"""


class InvalidTokenError(BaseSecurityException):
    """Exception raised when a token is invalid"""


class PasswordChangeError(BaseSecurityException):
    """Exception raised when a password is incorrect"""
