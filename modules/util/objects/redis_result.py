class RedisResult:
    """ Object representing redis result object
    """

    def __init__(self, status: bool):
        """ Constructor for RedisResult
        Args:
            status (bool):          Status of operation
        """
        self.__status: bool = status
        self.__value: str or None = None

    def get_status(self) -> bool:
        """ Get status
        Returns:
            bool
        """
        return self.__status

    def set_value(self, value: str):
        """ Set value
        Args:
            value (str):
        """
        self.__value = value

    def get_value(self) -> str:
        """ Get value
        Returns:
            str
        """
        return self.__value
