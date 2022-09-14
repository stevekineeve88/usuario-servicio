from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from tests.integration.setup.config.config import get_config


class ConnectionManagerFactoryTest(FactoryInterface):
    def __init__(self):
        config = get_config()
        self.__connection_manager: ConnectionManager = ConnectionManager(
            "test_connection_pool",
            10,
            host=config["MYSQL_DB_HOST"],
            port=config["MYSQL_DB_PORT"],
            user=config["MYSQL_DB_USER"],
            pwd=config["MYSQL_DB_PWD"],
            db=config["MYSQL_DB_NAME"],
        )

    def invoke(self, service_manager):
        return self.__connection_manager

    def get_connection_manager(self):
        return self.__connection_manager
