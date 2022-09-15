import datetime
from typing import Dict
import jwt
from modules.password.data.password_reset_data import PasswordResetData
from modules.password.exceptions.password_reset_create_exception import PasswordResetCreateException
from modules.password.exceptions.password_reset_delete_exception import PasswordResetDeleteException
from modules.password.exceptions.password_reset_fetch_exception import PasswordResetFetchException
from modules.password.objects.password_reset_token import PasswordResetToken


class PasswordResetManager:
    """ Manager for password reset objects
    """

    def __init__(self, **kwargs):
        """ Constructor for PasswordResetManager
        Args:
            **kwargs:   Dependencies
                password_reset_data (PasswordResetData)                 - Password reset data layer
                secret_key (str)                                        - Secret key
        """
        self.__password_reset_data: PasswordResetData = kwargs.get("password_reset_data")
        self.__secret_key: str = kwargs.get("secret_key")

    def create(self, user_id: int) -> PasswordResetToken:
        """ Create password reset token
        Args:
            user_id (int):          User ID
        Returns:
            PasswordResetToken
        """
        result = self.__password_reset_data.delete_by_user_id(user_id)
        if not result.get_status():
            raise PasswordResetDeleteException("Could not delete password reset token")

        token = jwt.encode({
            "sub:id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }, self.__secret_key, algorithm="HS256")
        result = self.__password_reset_data.insert(token, user_id)
        if not result.get_status():
            raise PasswordResetCreateException("Could not create password reset token")

        return PasswordResetToken(result.get_last_insert_id(), token, user_id)

    def get_by_token(self, token: str) -> PasswordResetToken:
        """ Get by token
        Args:
            token (str):            Password reset token
        Returns:
            PasswordResetToken
        """
        result = self.__password_reset_data.load_by_token(token)
        if result.get_affected_rows() == 0:
            raise PasswordResetFetchException("Could not find password reset token")

        data = result.get_data()[0]
        return PasswordResetToken(
            int(data["id"]),
            data["token"],
            int(data["user_id"])
        )

    def delete_by_user_id(self, user_id):
        """ Delete by user ID
        Args:
            user_id (int):
        """
        result = self.__password_reset_data.delete_by_user_id(user_id)
        if result.get_affected_rows() == 0:
            raise PasswordResetDeleteException("Could not delete password reset token")

    def verify_payload(self, token: str) -> Dict[str, any]:
        """ Verify payload of password reset token
        Args:
            token (str):            JWT token
        Returns:
            Dict[str, any]
        """
        return jwt.decode(token, self.__secret_key, algorithms=["HS256"], options={
            "require": [
                "sub:id",
                "exp"
            ]
        })
