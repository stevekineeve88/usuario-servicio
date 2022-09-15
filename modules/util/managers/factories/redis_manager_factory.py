from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface

from modules.util.managers.redis_manager import RedisManager


class RedisManagerFactory(FactoryInterface):
    """ Factory for generating redis manager object
    """

    def invoke(self, service_manager):
        return RedisManager()
