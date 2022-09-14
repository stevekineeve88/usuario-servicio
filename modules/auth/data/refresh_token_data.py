from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class RefreshTokenData:
    """ Data layer for refresh token data
    """

    def __init__(self, **kwargs):
        """ Constructor for RefreshTokenData
        Args:
            **kwargs:       Dependencies
                connection_manager (ConnectionManager) - Connection manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def insert(self, user_id: int, token: str) -> Result:
        """ Insert a refresh token
        Args:
            user_id (int):          User ID
            token (str):            JWT token
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO user_refresh_token (user_id, token)
            VALUES (%(user_id)s, %(token)s)
        """, {
            "user_id": user_id,
            "token": token
        })

    def load_by_token(self, token: str) -> Result:
        """ Load by token
        Args:
            token (str):            JWT token
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                user_refresh_token.id,
                user_refresh_token.token,
                user_refresh_token.user_id,
                user_refresh_token.created_timestamp
            FROM user_refresh_token
            WHERE user_refresh_token.token = %(token)s
        """, {
            "token": token
        })

    def delete_by_token(self, token: str) -> Result:
        """ Delete by token
        Args:
            token (str):            JWT token
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM user_refresh_token WHERE token = %(token)s
        """, {
            "token": token
        })

    def delete_by_user_id(self, user_id: int) -> Result:
        """ Delete by user ID
        Args:
            user_id (int):      User ID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM user_refresh_token WHERE user_id = %(user_id)s
        """, {
            "user_id": user_id
        })
