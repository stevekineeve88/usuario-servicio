from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.auth.data.refresh_token_data import RefreshTokenData


class RefreshTokenDataFactory(FactoryInterface):
    """ Factory for creating refresh token data object
    """

    def invoke(self, service_manager):
        return RefreshTokenData(
            connection_manager=service_manager.get(ConnectionManager.__name__)
        )
