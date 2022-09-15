import datetime
from typing import Dict
import jwt
from modules.auth.data.refresh_token_data import RefreshTokenData
from modules.auth.exceptions.refresh_token_create_exception import RefreshTokenCreateException
from modules.auth.exceptions.refresh_token_delete_exception import RefreshTokenDeleteException
from modules.auth.exceptions.refresh_token_fetch_exception import RefreshTokenFetchException


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
        self.__refresh_token_data: RefreshTokenData = kwargs.get("refresh_token_data")
        self.__secret_key: str = kwargs.get("secret_key")

    def create(self, user_id: int, user_uuid: str) -> str:
        """ Create refresh token
        Args:
            user_id (int):              User ID
            user_uuid (str):            User UUID
        Returns:
            str
        """
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=200)
        token = jwt.encode({
            "sub:id": user_id,
            "sub:uuid": user_uuid,
            "exp": expiration
        }, self.__secret_key, algorithm="HS256")
        result = self.__refresh_token_data.insert(
            user_uuid,
            token,
            int((expiration - datetime.datetime.now()).total_seconds())
        )
        if not result.get_status():
            raise RefreshTokenCreateException("Could not create refresh token")
        return token

    def get_by_user_uuid(self, user_uuid: str) -> str:
        """ Get by user UUID
        Args:
            user_uuid (str):            User UUID
        Returns:
            str
        """
        result = self.__refresh_token_data.load_by_user_uuid(user_uuid)
        if not result.get_status():
            raise RefreshTokenFetchException("Could not find refresh token")
        return result.get_value()

    def delete_by_user_uuid(self, user_uuid: str):
        """ Delete by user UUID
        Args:
            user_uuid (str):            User UUID
        """
        result = self.__refresh_token_data.delete_by_user_uuid(user_uuid)
        if not result.get_status():
            raise RefreshTokenDeleteException("Could not delete refresh token")

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
