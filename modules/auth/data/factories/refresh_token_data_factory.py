from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.auth.data.refresh_token_data import RefreshTokenData
from modules.util.managers.redis_manager import RedisManager


class RefreshTokenDataFactory(FactoryInterface):
    """ Factory for creating refresh token data object
    """

    def invoke(self, service_manager):
        return RefreshTokenData(
            redis_manager=service_manager.get(RedisManager.__name__)
        )
