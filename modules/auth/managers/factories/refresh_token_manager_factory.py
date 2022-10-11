import os
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.auth.managers.refresh_token_manager import RefreshTokenManager


class RefreshTokenManagerFactory(FactoryInterface):
    """ Factory for creating refresh token manager factory
    """

    def invoke(self, service_manager):
        return RefreshTokenManager(
            secret_key=os.environ["SECRET_KEY"]
        )
