import bcrypt
from modules.auth.exceptions.auth_password_exception import AuthPasswordException
from modules.auth.exceptions.auth_status_exception import AuthStatusException
from modules.auth.managers.access_token_manager import AccessTokenManager
from modules.auth.managers.refresh_token_manager import RefreshTokenManager
from modules.auth.objects.validation_token import ValidationToken
from modules.user.data.user_data import UserData
from modules.user.exceptions.user_fetch_exception import UserFetchException
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager


class AuthManager:
    """ Manager for authentication operations
    """

    def __init__(self, **kwargs):
        """ Constructor for AuthManager
        Args:
            **kwargs:       Dependencies
                user_data (UserData)                            - User daya layer
                user_manager (UserManager)                      - User object manager
                status_manager (StatusManager)                  - Status object manager
                refresh_token_manager (RefreshTokenManager)     - Refresh token object manager
                access_token_manager (AccessTokenManager)       - Access token object manager
        """
        self.__user_data: UserData = kwargs.get("user_data")
        self.__user_manager: UserManager = kwargs.get("user_manager")
        self.__status_manager: StatusManager = kwargs.get("status_manager")
        self.__refresh_token_manager: RefreshTokenManager = kwargs.get("refresh_token_manager")
        self.__access_token_manager: AccessTokenManager = kwargs.get("access_token_manager")

    def authenticate(self, email: str, password: str) -> ValidationToken:
        """ Authenticate user
        Args:
            email (str):
            password (str):
        Returns:
            ValidationToken
        """
        result = self.__user_data.load_auth_info_by_email(email)
        if result.get_affected_rows() == 0:
            raise UserFetchException(f"User not found with email {email}")

        user_auth_info = result.get_data()[0]
        if not bcrypt.checkpw(password.encode(), user_auth_info["password"].encode()):
            raise AuthPasswordException(f"Authentication failed")

        user = self.__user_manager.get_by_id(user_auth_info["id"])
        if user.get_status().get_id() != self.__status_manager.get_by_const("ACTIVE").get_id():
            raise AuthStatusException(f"User is not active")

        self.__refresh_token_manager.delete_by_user_id(user.get_id())
        access_token = self.__access_token_manager.create(user)
        refresh_token = self.__refresh_token_manager.create(user)
        return ValidationToken(refresh_token, access_token)

    def generate_validation_token(self, refresh_token_str: str) -> ValidationToken:
        """ Generate validation token from refresh token
        Args:
            refresh_token_str (str):            Valid refresh token
        Returns:
            ValidationToken
        """
        self.__refresh_token_manager.verify_payload(refresh_token_str)

        old_refresh_token_obj = self.__refresh_token_manager.get(refresh_token_str)
        user = self.__user_manager.get_by_id(old_refresh_token_obj.get_user_id())
        if user.get_status().get_id() != self.__status_manager.get_by_const("ACTIVE").get_id():
            raise AuthStatusException(f"User is not active")

        access_token = self.__access_token_manager.create(user)
        new_refresh_token_obj = self.__refresh_token_manager.create(user)
        self.__refresh_token_manager.delete_by_token(refresh_token_str)

        return ValidationToken(new_refresh_token_obj, access_token)

