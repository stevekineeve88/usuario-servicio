import datetime
from typing import Dict
import jwt


class RefreshTokenManager:
    """ Manages refresh token manager objects
    """

    def __init__(self, **kwargs):
        """ Constructor for RefreshTokenManager
        Args:
            **kwargs:       Dependencies
                refresh_token_data (RefreshTokenData)               - Refresh token data layer
                secret_key (str)                                    - Secret key
        """
        self.__secret_key: str = kwargs.get("secret_key")

    def create(self, user_id: int, user_uuid: str) -> str:
        """ Create refresh token
        Args:
            user_id (int):              User ID
            user_uuid (str):            User UUID
        Returns:
            str
        """
        return jwt.encode({
            "sub:id": user_id,
            "sub:uuid": user_uuid,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=200)
        }, self.__secret_key, algorithm="HS256")

    def verify_payload(self, token: str) -> Dict[str, any]:
        """ Verify payload
        Args:
            token (str):            JWT token
        Returns:
            Dict[str, any]
        """
        return jwt.decode(token, self.__secret_key, algorithms=["HS256"], options={
            "require": [
                "sub:id",
                "sub:uuid",
                "exp"
            ]
        })
