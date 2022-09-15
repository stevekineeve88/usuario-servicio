import datetime
from typing import Dict
import jwt


class AccessTokenManager:
    """ Manager for access token objects
    """

    def __init__(self, **kwargs):
        """ Constructor for AccessTokenManager
        Args:
            **kwargs:           Dependencies
                secret_key (str) - Secret key
        """
        self.__secret_key = kwargs.get("secret_key")

    def create(self, **kwargs) -> str:
        """ Create access token
        Args:
            kwargs:        Token info
                user_id (int)               - User ID
                user_email (str)            - User email
                user_uuid (str)             - User UUID
        Returns:
            str
        """
        return jwt.encode({
            "sub:id": kwargs.get("user_id"),
            "sub:email": kwargs.get("user_email"),
            "sub:uuid": kwargs.get("user_uuid"),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, self.__secret_key, algorithm="HS256")

    def verify_payload(self, token: str) -> Dict[str, any]:
        """ Verify payload of access token
        Args:
            token (str):            JWT token
        Returns:
            Dict[str, any]
        """
        return jwt.decode(token, self.__secret_key, algorithms=["HS256"], options={
            "require": [
                "sub:id",
                "sub:email",
                "sub:uuid",
                "exp"
            ]
        })
