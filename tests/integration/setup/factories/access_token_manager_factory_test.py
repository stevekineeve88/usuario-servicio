from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.auth.managers.access_token_manager import AccessTokenManager
from tests.integration.setup.config.config import get_config


class AccessTokenManagerFactoryTest(FactoryInterface):
    def invoke(self, service_manager):
        config = get_config()
        return AccessTokenManager(
            secret_key=config["SECRET_KEY"]
        )
