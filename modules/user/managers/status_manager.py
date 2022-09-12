from typing import List, Dict
from modules.user.data.status_data import StatusData
from modules.user.exceptions.user_status_fetch_exception import UserStatusFetchException
from modules.user.objects.status import Status


class StatusManager:
    """ Manager for status objects
    """

    def __init__(self, **kwargs):
        """ Constructor for StatusManager
        Args:
            **kwargs:  Dependencies
                status_data (StatusData) - User status data layer
        """
        self.__status_data: StatusData = kwargs.get("status_data")

        self.__status_cache: Dict[int, Status] = {}
        self.__status_id_cache: Dict[str, int] = {}

    def get_all(self) -> List[Status]:
        """ Get all user statuses
        Returns:
            List[Status]
        """
        if len(self.__status_cache) > 0:
            return list(self.__status_cache.values())

        result = self.__status_data.load_all()
        if result.get_affected_rows() == 0:
            raise UserStatusFetchException("Could not fetch user statuses")

        statuses: List[Status] = []
        data = result.get_data()
        for datum in data:
            statuses.append(self.__build_status(datum))
        self.__cache_all(statuses)
        return statuses

    def get_by_id(self, status_id: int) -> Status:
        """ Get by ID
        Args:
            status_id (int):        Status ID
        Returns:
            Status
        """
        if status_id in self.__status_cache:
            return self.__status_cache[status_id]

        self.get_all()
        if status_id not in self.__status_cache:
            raise UserStatusFetchException(f"Unknown status ID {status_id}")
        return self.__status_cache[status_id]

    def get_by_const(self, const: str) -> Status:
        """ Get by constant
        Args:
            const (str):        Status constant
        Returns:
            Status
        """
        if const in self.__status_id_cache:
            return self.__status_cache[self.__status_id_cache[const]]

        self.get_all()
        if const not in self.__status_id_cache:
            raise UserStatusFetchException(f"Unknown status constant {const}")
        return self.__status_cache[self.__status_id_cache[const]]

    @classmethod
    def __build_status(cls, data: Dict[str, any]) -> Status:
        """ Build user status object
        Args:
            data (Dict[str, any]):      Dict representation of user status
        Returns:
            Status
        """
        return Status(
            data["id"],
            data["const"],
            data["description"]
        )

    def __cache(self, status: Status):
        """ Cache status
        Args:
            status (Status):
        """
        self.__status_cache[status.get_id()] = status
        self.__status_id_cache[status.get_const()] = status.get_id()

    def __cache_all(self, statuses: List[Status]):
        """ Cache list of statuses
        Args:
            statuses (List[Status]):
        """
        for status in statuses:
            self.__cache(status)
