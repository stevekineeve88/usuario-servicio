from typing import Dict
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.password.data.factories.password_reset_data_factory import PasswordResetDataFactory
from modules.password.data.password_reset_data import PasswordResetData
from modules.password.managers.factories.password_reset_manager_factory import PasswordResetManagerFactory
from modules.password.managers.password_reset_manager import PasswordResetManager


class PasswordConfig:
    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            PasswordResetData.__name__: PasswordResetDataFactory(),
            PasswordResetManager.__name__: PasswordResetManagerFactory()
        }
