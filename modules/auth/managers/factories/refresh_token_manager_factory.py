import os
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.auth.data.refresh_token_data import RefreshTokenData
from modules.auth.managers.refresh_token_manager import RefreshTokenManager


class RefreshTokenManagerFactory(FactoryInterface):
    """ Factory for creating refresh token manager factory
    """

    def invoke(self, service_manager):
        return RefreshTokenManager(
            refresh_token_data=service_manager.get(RefreshTokenData.__name__),
            secret_key=os.environ["SECRET_KEY"]
        )
