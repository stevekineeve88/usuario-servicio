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

    def get_all(self) -> List[Status]:
        """ Get all user statuses
        Returns:
            List[Status]
        """
        result = self.__status_data.load_all()
        if result.get_affected_rows() == 0:
            raise UserStatusFetchException("Could not fetch user statuses")

        statuses: List[Status] = []
        data = result.get_data()
        for datum in data:
            statuses.append(self.__build_status(datum))
        return statuses

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
