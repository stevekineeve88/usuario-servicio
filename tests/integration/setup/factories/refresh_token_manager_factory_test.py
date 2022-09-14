from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.auth.data.refresh_token_data import RefreshTokenData
from modules.auth.managers.refresh_token_manager import RefreshTokenManager
from tests.integration.setup.config.config import get_config


class RefreshTokenManagerFactoryTest(FactoryInterface):
    def invoke(self, service_manager):
        config = get_config()
        return RefreshTokenManager(
            refresh_token_data=service_manager.get(RefreshTokenData.__name__),
            secret_key=config["SECRET_KEY"]
        )
