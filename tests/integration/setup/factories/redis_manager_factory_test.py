from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.util.managers.redis_manager import RedisManager
from tests.integration.setup.config.config import get_config


class RedisManagerFactoryTest(FactoryInterface):
    def invoke(self, service_manager):
        config = get_config()
        return RedisManager(
            host=config["REDIS_HOST"],
            port=config["REDIS_PORT"],
            pwd=config["REDIS_PWD"],
            db=1,
        )
