from typing import Dict

from sk88_http_response.modules.http.interfaces.http_dict import HTTPDict


class Status(HTTPDict):
    """ Object representation of status
    """

    def __init__(self, status_id: int, const: str, description: str):
        """ Constructor for Status
        Args:
            status_id (int):        User status ID
            const (str):            User status constant
            description (str):      User status description
        """
        self.__id: int = status_id
        self.__const: str = const
        self.__description: str = description

    def get_id(self) -> int:
        """ Get ID
        Returns:
            int
        """
        return self.__id

    def get_const(self) -> str:
        """ Get constant
        Returns:
            str
        """
        return self.__const

    def get_description(self) -> str:
        """ Get description
        Returns:
            str
        """
        return self.__description

    def get_http_dict(self) -> Dict[str, any]:
        """ Get user status HTTP dict
        Returns:
            Dict[str, any]
        """
        return {
            "id": self.get_id(),
            "const": self.get_const(),
            "description": self.get_description()
        }
