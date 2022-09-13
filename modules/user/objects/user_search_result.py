from typing import List
from modules.user.objects.user import User


class UserSearchResult:
    """ Object representing user search result
    """

    def __init__(self, users: List[User], total_count):
        """ Constructor for UserSearchResult
        Args:
            users (List[User]):         User list of search
            total_count (int):          Total un-paginated count
        """
        self.__users: List[User] = users
        self.__total_count: int = total_count

    def get_users(self) -> List[User]:
        """ Get users
        Returns:
            List[User]
        """
        return self.__users

    def get_total_count(self) -> int:
        """ Get total count
        Returns:
            int
        """
        return self.__total_count
