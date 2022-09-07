from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class StatusData:
    """ Data layer for user statuses
    """

    def __init__(self, **kwargs):
        """ Constructor for StatusData
        Args:
            **kwargs:   Dependencies
                connection_manager (ConnectionManager) - Database manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def load_all(self) -> Result:
        """ Load all statuses
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                user_status.id,
                user_status.const,
                user_status.description
            FROM user_status
        """)
