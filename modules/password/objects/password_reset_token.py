class PasswordResetToken:
    """ Object representing password reset token
    """

    def __init__(self, token_id: int, token: str, user_id: int):
        """ Constructor for password reset token
        Args:
            token_id (int):             Token ID
            token (str):                Reset JWT token
            user_id (int):              User ID
        """
        self.__id: int = token_id
        self.__token: str = token
        self.__user_id: int = user_id

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
