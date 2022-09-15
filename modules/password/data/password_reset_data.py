from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class PasswordResetData:
    """ Data layer for password reset data
    """

    def __init__(self, **kwargs):
        """ Constructor for PasswordResetData
        Args:
            **kwargs:       Dependencies
                connection_manager (ConnectionManager)      - Connection manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def insert(self, token: str, user_id: int) -> Result:
        """ Insert password reset token
        Args:
            token (str):            JWT token
            user_id (int):          User ID
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO password_reset (token, user_id)
            VALUES (%(token)s, %(user_id)s)
        """, {
            "token": token,
            "user_id": user_id
        })

    def delete_by_user_id(self, user_id: int) -> Result:
        """ Delete by user ID
        Args:
            user_id (int):
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM password_reset WHERE user_id = %(user_id)s
        """, {
            "user_id": user_id
        })

    def load_by_token(self, token: str) -> Result:
        """ Load by password reset token
        Args:
            token (str):           JWT token
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                password_reset.id,
                password_reset.token,
                password_reset.user_id
            FROM password_reset
            WHERE password_reset.token = %(token)s
        """, {
            "token": token
        })
