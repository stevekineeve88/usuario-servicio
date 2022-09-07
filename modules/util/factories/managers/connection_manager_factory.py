from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface


class ConnectionManagerFactory(FactoryInterface):
    """ Connection manager factory for building connection manager
    """

    def invoke(self, service_manager) -> ConnectionManager:
        return ConnectionManager("user_service_pool", 10)
