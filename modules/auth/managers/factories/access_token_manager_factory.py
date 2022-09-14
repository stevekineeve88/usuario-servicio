import os

from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.auth.managers.access_token_manager import AccessTokenManager


class AccessTokenManagerFactory(FactoryInterface):
    """ Factory for creating access token manager object
    """

    def invoke(self, service_manager):
        return AccessTokenManager(
            secret_key=os.environ["SECRET_KEY"]
        )
