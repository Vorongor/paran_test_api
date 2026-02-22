from abc import ABC, abstractmethod


class JWTAuthManagerInterface(ABC):
    """
    Interface for JWT Authentication Manager.
    Defines methods for decoding, and verifying JWT tokens.
    """

    @abstractmethod
    def decode_access_token(self, token: str) -> dict[str, object]:
        """
        Decode and validate an access token.
        """
        pass

    @abstractmethod
    def verify_access_token_or_raise(self, token: str) -> None:
        """
        Verify an access token or raise an error if invalid.
        """
        pass
