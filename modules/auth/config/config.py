from typing import Dict
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.auth.data.factories.refresh_token_data_factory import RefreshTokenDataFactory
from modules.auth.data.refresh_token_data import RefreshTokenData
from modules.auth.managers.access_token_manager import AccessTokenManager
from modules.auth.managers.auth_manager import AuthManager
from modules.auth.managers.factories.access_token_manager_factory import AccessTokenManagerFactory
from modules.auth.managers.factories.auth_manager_factory import AuthManagerFactory
from modules.auth.managers.factories.refresh_token_manager_factory import RefreshTokenManagerFactory
from modules.auth.managers.refresh_token_manager import RefreshTokenManager


class AuthConfig:
    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            RefreshTokenData.__name__: RefreshTokenDataFactory(),
            RefreshTokenManager.__name__: RefreshTokenManagerFactory(),
            AuthManager.__name__: AuthManagerFactory(),
            AccessTokenManager.__name__: AccessTokenManagerFactory()
        }
