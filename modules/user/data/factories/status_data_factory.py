from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface

from modules.user.data.status_data import StatusData


class StatusDataFactory(FactoryInterface):
    """ Factory for creating status data object
    """

    def invoke(self, service_manager):
        return StatusData(
            connection_manager=service_manager.get(ConnectionManager.__name__)
        )
