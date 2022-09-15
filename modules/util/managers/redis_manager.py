import os
import redis
from modules.util.objects.redis_result import RedisResult


class RedisManager:
    """ Manager for Redis operations
    """

    def __init__(self, **kwargs):
        """ Constructor for RedisManager
        Args:
            **kwargs:       Dependencies
                host (str)          - [Optional]    Redis host
                port (int)          - [Optional]    Redis port number
                pwd (str)           - [Optional]    Redis connection password
                db (int)            - [Optional]    Redis DB (For testing purposes)
        """
        self.__host = kwargs.get("host") or os.environ["REDIS_HOST"]
        self.__port = kwargs.get("port") or os.environ["REDIS_PORT"]
        self.__pwd = kwargs.get("pwd") or os.environ["REDIS_PWD"]
        self.__redis = redis.Redis(
            host=self.__host,
            port=self.__port,
            password=self.__pwd,
            db=kwargs.get("db") or 0
        )

    def get_connection(self) -> redis.Redis:
        """ Get connection
        Returns:
            redis.Redis
        """
        return self.__redis

    def set(self, key: str, value: str, expy: int = None) -> RedisResult:
        """ Set key and value
        Args:
            key (str):          Key value
            value (str):        Value associated with key
            expy (int):         [Optional] expiry of row in seconds
        Returns:
            RedisResult
        """
        return RedisResult(self.__redis.set(key, value, ex=expy))

    def get(self, key: str) -> RedisResult:
        """ Get value by key
        Args:
            key (str):          Key value
        Returns:
            RedisResult
        """
        value = self.__redis.get(key)
        if value is None:
            return RedisResult(False)
        redis_result = RedisResult(True)
        redis_result.set_value(value.decode())
        return redis_result

    def delete(self, key: str) -> RedisResult:
        """ Delete by key
        Args:
            key (str):          Key value
        Returns:
            RedisResult
        """
        result = self.__redis.delete(key)
        if result < 1:
            return RedisResult(False)
        return RedisResult(True)
