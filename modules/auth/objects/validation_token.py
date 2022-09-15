from typing import Dict
from sk88_http_response.modules.http.interfaces.http_dict import HTTPDict


class ValidationToken(HTTPDict):
    """ Object representing a validation token object
    """

    def __init__(self, refresh_token: str, access_token: str):
        """ Constructor for ValidationToken
        Args:
            refresh_token (str):                Refresh token
            access_token (str):                 Access token
        """
        self.__refresh_token: str = refresh_token
        self.__access_token: str = access_token

    def get_refresh_token(self) -> str:
        """ Get refresh token
        Returns:
            str
        """
        return self.__refresh_token

    def get_access_token(self) -> str:
        """ Get access token
        Returns:
            str
        """
        return self.__access_token

    def get_http_dict(self) -> Dict[str, any]:
        """ Get http dict of validation token
        Returns:
            Dict[str, any]
        """
        return {
            "refresh_token": self.get_refresh_token(),
            "access_token": self.get_access_token()
        }
