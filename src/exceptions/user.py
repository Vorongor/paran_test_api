class UserBaseException(Exception):

    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Something went wrong during account operation"
        super().__init__(message)


class UserCreateException(UserBaseException):
    pass


class UserAlreadyExistsException(UserBaseException):
    pass


class UserNotFoundException(UserBaseException):
    pass
