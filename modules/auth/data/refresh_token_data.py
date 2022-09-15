from modules.util.managers.redis_manager import RedisManager
from modules.util.objects.redis_result import RedisResult


class RefreshTokenData:
    """ Data layer for refresh token data
    """

    def __init__(self, **kwargs):
        """ Constructor for RefreshTokenData
        Args:
            **kwargs:       Dependencies
                connection_manager (ConnectionManager) - Connection manager
        """
        self.__redis_manager: RedisManager = kwargs.get("redis_manager")

    def insert(self, user_uuid: str, token: str, expiry: int) -> RedisResult:
        """ Insert a refresh token
        Args:
            user_uuid (int):        User UUID
            token (str):            JWT token
            expiry (int):           Expiry in seconds
        Returns:
            RedisResult
        """
        return self.__redis_manager.set(user_uuid, token, expiry)

    def load_by_user_uuid(self, user_uuid: str) -> RedisResult:
        """ Load by user UUID
        Args:
            user_uuid (str):            User UUID
        Returns:
            RedisResult
        """
        return self.__redis_manager.get(user_uuid)

    def delete_by_user_uuid(self, user_uuid: str) -> RedisResult:
        """ Delete by user UUID
        Args:
            user_uuid (str):            User UUID
        Returns:
            RedisResult
        """
        return self.__redis_manager.delete(user_uuid)
