from datetime import datetime


class RefreshToken:
    """ Object representing a refresh token
    """

    def __init__(self, **kwargs):
        """ Constructor for RefreshToken
        Args:
            **kwargs:   refresh token info
                id (int)                        - Refresh token ID
                token (str)                     - Refresh token
                user_id (int)                   - User ID
                created_timestamp (datetime)    - Created timestamp
        """
        self.__id: int = kwargs.get("id")
        self.__token: str = kwargs.get("token")
        self.__user_id: int = kwargs.get("user_id")
        self.__created_timestamp: datetime = kwargs.get("created_timestamp")

    def get_id(self) -> int:
        """ Get ID
        Returns:
            int
        """
        return self.__id

    def get_token(self) -> str:
        """ Get token
        Returns:
            str
        """
        return self.__token

    def get_user_id(self) -> int:
        """ Get user ID
        Returns:
            int
        """
        return self.__user_id

    def get_created_timestamp(self) -> datetime:
        """ Get created timestamp
        Returns:
            datetime
        """
        return self.__created_timestamp
