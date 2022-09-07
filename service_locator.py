from sk88_service_locator.modules.service.managers.service_manager import ServiceManager
from modules.user.config.config import UserConfig
from modules.util.config.config import UtilConfig


service_locator: ServiceManager or None = None


def get_service_manager() -> ServiceManager:
    """ Get service manager
    Returns:
        ServiceManager
    """
    global service_locator

    if service_locator is None:
        service_locator = ServiceManager()
        service_locator.add(UserConfig().get())
        service_locator.add(UtilConfig().get())

    return service_locator
