from typing import Dict
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.util.managers.factories.connection_manager_factory import ConnectionManagerFactory
from modules.util.managers.factories.redis_manager_factory import RedisManagerFactory
from modules.util.managers.redis_manager import RedisManager


class UtilConfig:

    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            ConnectionManager.__name__: ConnectionManagerFactory(),
            RedisManager.__name__: RedisManagerFactory(),
        }
