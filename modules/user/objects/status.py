class Status:
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
