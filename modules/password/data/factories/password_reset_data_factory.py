from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.password.data.password_reset_data import PasswordResetData


class PasswordResetDataFactory(FactoryInterface):
    """ Factory for password reset data object
    """

    def invoke(self, service_manager):
        return PasswordResetData(
            connection_manager=service_manager.get(ConnectionManager.__name__)
        )
