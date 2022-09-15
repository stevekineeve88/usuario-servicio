from typing import Tuple, Dict

from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class UserData:
    """ Data layer for users
    """

    def __init__(self, **kwargs):
        """ Constructor for UserData
        Args:
            **kwargs:   Dependencies
                connection_manager (ConnectionManager) - Database manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def insert(self, status_id: int, **kwargs) -> Result:
        """ Insert user
        Args:
            status_id (int):        Status ID
            **kwargs:               User information
                first_name (str)
                last_name (str)
                email (str)
                password (bytes)          - Encrypted password
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO user (first_name, last_name, email, password, status_id)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(status_id)s)
        """, {
            "first_name": kwargs.get("first_name"),
            "last_name": kwargs.get("last_name"),
            "email": kwargs.get("email"),
            "password": kwargs.get("password"),
            "status_id": status_id,
        })

    def load_by_id(self, user_id: int) -> Result:
        """ Load by ID
        Args:
            user_id (int):      User ID
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                user.id,
                bin_to_uuid(user.uuid) as uuid,
                user.first_name,
                user.last_name,
                user.email,
                user.status_id,
                user.created_timestamp,
                user.update_timestamp
            FROM user
            WHERE user.id = %(id)s
        """, {
            "id": user_id
        })

    def load_by_email(self, email: str) -> Result:
        """ Load by email
        Args:
            email (str):
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                user.id,
                bin_to_uuid(user.uuid) as uuid,
                user.first_name,
                user.last_name,
                user.email,
                user.status_id,
                user.created_timestamp,
                user.update_timestamp
            FROM user
            WHERE user.email = %(email)s
        """, {
            "email": email
        })

    def load_auth_info_by_email(self, email: str) -> Result:
        """ Load authentication information by user email
        Args:
            email (str):            User email
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                user.id,
                bin_to_uuid(user.uuid) as uuid,
                user.email,
                user.password,
                user.status_id
            FROM user
            WHERE user.email = %(email)s
        """, {
            "email": email
        })

    def update(self, user_id: int, **kwargs) -> Result:
        """ Update user information
        Args:
            user_id (int):          User ID
            **kwargs:               User information to update
                first_name (str)
                last_name (str)
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            UPDATE user SET first_name = %(first_name)s,
            last_name = %(last_name)s
            WHERE id = %(id)s
        """, {
            "first_name": kwargs.get("first_name"),
            "last_name": kwargs.get("last_name"),
            "id": user_id
        })

    def update_status(self, user_id: int, status_id: int) -> Result:
        """ Update user status
        Args:
            user_id (int):      User ID
            status_id (int):    Status ID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            UPDATE user SET status_id = %(status_id)s
            WHERE id = %(id)s
        """, {
            "status_id": status_id,
            "id": user_id
        })

    def update_password(self, user_id: int, password: bytes) -> Result:
        """ Update user password
        Args:
            user_id (int):          User ID
            password (str):         Encrypted password
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            UPDATE user SET password = %(password)s
            WHERE id = %(id)s
        """, {
            "password": password,
            "id": user_id
        })

    def delete(self, user_id: int) -> Result:
        """ Delete user
        Args:
            user_id (int):      User ID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM user WHERE id = %(id)s
        """, {
            "id": user_id
        })

    def search(self, **kwargs) -> Result:
        """ Search users
        Args:
            **kwargs:           Search params
                search (str)
                limit (int)
                offset (int)
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                user.id,
                bin_to_uuid(user.uuid) as uuid,
                user.first_name,
                user.last_name,
                user.email,
                user.status_id,
                user.created_timestamp,
                user.update_timestamp
            FROM user
            {self.__build_search_query()}
            ORDER BY user.last_name ASC
            LIMIT %(limit)s OFFSET %(offset)s
        """, {
            "search": f"%{kwargs.get('search')}%",
            "limit": kwargs.get("limit"),
            "offset": kwargs.get("offset")
        })

    def search_count(self, search) -> Result:
        """ Get count of search
        Args:
            search (str):
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                COUNT(*) AS count
            FROM user
            {self.__build_search_query()}
        """, {
            "search": f"%{search}%"
        })

    @classmethod
    def __build_search_query(cls) -> str:
        """ Build search query for users
        Returns:
            str
        """
        return f"""
            WHERE user.first_name LIKE %(search)s
                OR user.last_name LIKE %(search)s
                OR user.email LIKE %(search)s
        """
