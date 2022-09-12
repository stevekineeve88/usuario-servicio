from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.user.data.user_data import UserData
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager


class UserManagerFactory(FactoryInterface):
    """ Factory for creating user manager object
    """

    def invoke(self, service_manager):
        return UserManager(
            user_data=service_manager.get(UserData.__name__),
            status_manager=service_manager.get(StatusManager.__name__)
        )
