from datetime import datetime
from typing import Dict
from sk88_http_response.modules.http.interfaces.http_dict import HTTPDict
from modules.user.objects.status import Status


class User(HTTPDict):
    """ Object for representation of user
    """

    def __init__(self, status: Status, **kwargs):
        """ Constructor for User
        Args:
            status (Status):
            **kwargs:               User information
                id (str)                        - User ID
                uuid (str)                      - User UUID
                email (str)                     - User email
                first_name (str)                - User first name
                last_name (str)                 - User last name
                created_timestamp (datetime)    - Created timestamp
                update_timestamp (datetime)     - Updated timestamp
        """
        self.__id: int = kwargs.get("id")
        self.__uuid: str = kwargs.get("uuid")
        self.__email: str = kwargs.get("email")
        self.__first_name: str = kwargs.get("first_name")
        self.__last_name: str = kwargs.get("last_name")
        self.__status: Status = status
        self.__created_timestamp: datetime = kwargs.get("created_timestamp")
        self.__update_timestamp: datetime = kwargs.get("update_timestamp")

    def get_id(self) -> int:
        """ Get ID
        Returns:
            int
        """
        return self.__id

    def get_uuid(self) -> str:
        """ Get UUID
        Returns:
            str
        """
        return self.__uuid

    def get_email(self) -> str:
        """ Get email
        Returns:
            str
        """
        return self.__email

    def get_first_name(self) -> str:
        """ Get first name
        Returns:
            str
        """
        return self.__first_name

    def set_first_name(self, first_name: str):
        """ Set first name
        Args:
            first_name (str):
        """
        self.__first_name = first_name

    def get_last_name(self) -> str:
        """ Get last name
        Returns:
            str
        """
        return self.__last_name

    def set_last_name(self, last_name: str):
        """ Set last name
        Args:
            last_name (str):
        """
        self.__last_name = last_name

    def get_status(self) -> Status:
        """ Get status
        Returns:
            Status
        """
        return self.__status

    def get_created_timestamp(self) -> datetime:
        """ Get created timestamp
        Returns:
            datetime
        """
        return self.__created_timestamp

    def get_update_timestamp(self) -> datetime:
        """ Get updated timestamp
        Returns:
            datetime
        """
        return self.__update_timestamp

    def get_http_dict(self) -> Dict[str, any]:
        """ Get user HTTP dict
        Returns:
            Dict[str, any]
        """
        date_format = "%Y-%m-%d %H:%M:%S"
        status = self.get_status()
        return {
            "id": self.get_id(),
            "uuid": self.get_uuid(),
            "email": self.get_email(),
            "first_name": self.get_first_name(),
            "last_name": self.get_last_name(),
            "status": {
                "id": status.get_id(),
                "const": status.get_const()
            },
            "create_timestamp": self.get_created_timestamp().strftime(date_format),
            "update_timestamp": self.get_update_timestamp().strftime(date_format)
        }
