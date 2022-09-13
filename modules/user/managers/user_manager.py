from typing import Dict, List

from modules.user.data.user_data import UserData
from modules.user.exceptions.user_create_exception import UserCreateException
from modules.user.exceptions.user_delete_exception import UserDeleteException
from modules.user.exceptions.user_fetch_exception import UserFetchException
from modules.user.exceptions.user_update_exception import UserUpdateException
from modules.user.managers.status_manager import StatusManager
from modules.user.objects.status import Status
from modules.user.objects.user import User
from modules.user.objects.user_search_result import UserSearchResult
import bcrypt


class UserManager:
    """ Manager for user objects
    """

    def __init__(self, **kwargs):
        """ Constructor for UserManager
        Args:
            **kwargs:       Dependencies
                user_data (UserData)                - User data layer
                status_manager (StatusManager)      - Status object manager
        """
        self.__user_data: UserData = kwargs.get("user_data")
        self.__status_manager: StatusManager = kwargs.get("status_manager")

    def create(self, status: Status, **kwargs) -> User:
        """ Create user
        Args:
            status (Status):        Status of user on creation
            **kwargs:               User Information
                first_name (str)        - First name of user
                last_name (str)         - Last name of user
                email (str)             - Email address of user
                password (str)          - Unencrypted password of user
        Returns:
            User
        """
        password: str = kwargs.get("password")
        result = self.__user_data.insert(
            status.get_id(),
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            email=kwargs.get("email"),
            password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        )
        if not result.get_status():
            raise UserCreateException(f"Could not create user: {result.get_message()}")
        return self.get_by_id(result.get_last_insert_id())

    def get_by_id(self, user_id: int) -> User:
        """ Get user by ID
        Args:
            user_id (int):          User ID
        Returns:
            User
        """
        result = self.__user_data.load_by_id(user_id)
        if result.get_affected_rows() == 0:
            raise UserFetchException(f"Could not find user with ID {user_id}")
        return self.__build_user(result.get_data()[0])

    def update(self, user: User) -> User:
        """ Update user
        Args:
            user (User):        User object to update
        """
        result = self.__user_data.update(
            user.get_id(),
            first_name=user.get_first_name(),
            last_name=user.get_last_name()
        )
        if not result.get_status():
            raise UserUpdateException(f"Could not update user with ID {user.get_id()}")
        return self.get_by_id(user.get_id())

    def update_status(self, user_id: int, status: Status) -> User:
        """ Update user status
        Args:
            user_id (int):      User ID
            status (Status):    New user status
        Returns:
            User
        """
        result = self.__user_data.update_status(user_id, status.get_id())
        if not result.get_status():
            raise UserUpdateException(f"Could not update status of user with ID {user_id}")
        return self.get_by_id(user_id)

    def delete(self, user_id: int):
        """ Delete user by ID
        Args:
            user_id (int):          User ID
        """
        result = self.__user_data.delete(user_id)
        if result.get_affected_rows() == 0:
            raise UserDeleteException(f"Could not delete user with ID {user_id}")

    def search(self, **kwargs) -> UserSearchResult:
        """ Search user table
        Args:
            **kwargs:       Search arguments
                search (str)        - [OPTIONAL] search string
                limit (int)         - [OPTIONAL] limit of result
                offset (int)        - [OPTIONAL] offset of result
        Returns:
            UserSearchResult
        """
        limit = kwargs.get("limit") or 100
        limit = limit if 100 >= limit > 0 else 10

        offset = kwargs.get("offset") or 0
        offset = offset if offset >= 0 else 0

        search = kwargs.get("search") or ""

        result = self.__user_data.search(
            search=search,
            limit=limit,
            offset=offset
        )
        if not result.get_status():
            raise UserFetchException(f"Could not search users: {result.get_message()}")

        data = result.get_data()
        users: List[User] = []
        for datum in data:
            users.append(self.__build_user(datum))

        result = self.__user_data.search_count(search)
        if not result.get_status():
            raise UserFetchException(f"Could not fetch user count: {result.get_message()}")

        return UserSearchResult(users, result.get_data()[0]["count"])

    def __build_user(self, data: Dict[str, any]) -> User:
        """ Build user object
        Args:
            data (DICT[str, any]):
        Returns:
            User
        """
        return User(
            self.__status_manager.get_by_id(data["status_id"]),
            id=data["id"],
            uuid=data["uuid"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            created_timestamp=data["created_timestamp"],
            update_timestamp=data["update_timestamp"],
        )
