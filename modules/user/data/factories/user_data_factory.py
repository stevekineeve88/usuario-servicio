from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface

from modules.user.data.user_data import UserData


class UserDataFactory(FactoryInterface):
    """ Factory for creating user data object
    """

    def invoke(self, service_manager):
        return UserData(
            connection_manager=service_manager.get(ConnectionManager.__name__)
        )
