from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface

from modules.auth.managers.access_token_manager import AccessTokenManager
from modules.auth.managers.auth_manager import AuthManager
from modules.auth.managers.refresh_token_manager import RefreshTokenManager
from modules.user.data.user_data import UserData
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager


class AuthManagerFactory(FactoryInterface):
    """ Factory for creating authentication manager object
    """

    def invoke(self, service_manager):
        return AuthManager(
            user_data=service_manager.get(UserData.__name__),
            user_manager=service_manager.get(UserManager.__name__),
            status_manager=service_manager.get(StatusManager.__name__),
            refresh_token_manager=service_manager.get(RefreshTokenManager.__name__),
            access_token_manager=service_manager.get(AccessTokenManager.__name__)
        )
