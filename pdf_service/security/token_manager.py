from typing import cast, Any

from jose import jwt, JWTError, ExpiredSignatureError

from pdf_service.security.exceptions import TokenExpiredError, InvalidTokenError
from pdf_service.security.interfaces import JWTAuthManagerInterface


class JWTAuthManager(JWTAuthManagerInterface):
    """
    A manager for creating, decoding, and verifying JWT access
    and refresh tokens.
    """

    def __init__(self, secret_key_access: str, secret_key_refresh: str, algorithm: str):
        """
        Initialize the manager with secret keys and algorithm for token
        operations.
        """
        self._secret_key_access = secret_key_access
        self._secret_key_refresh = secret_key_refresh
        self._algorithm = algorithm

    def decode_access_token(self, token: str) -> dict[str, object]:
        """
        Decode and validate an access token, returning the token's data.
        """
        try:
            payload = jwt.decode(
                token, self._secret_key_access, algorithms=[self._algorithm]
            )
            return cast(dict[str, Any], payload)
        except ExpiredSignatureError:
            raise TokenExpiredError
        except JWTError:
            raise InvalidTokenError

    def verify_access_token_or_raise(self, token: str) -> None:
        """
        Verify an access token and raise an error if it's invalid or expired.
        """
        self.decode_access_token(token)
