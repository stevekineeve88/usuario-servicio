from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.password.data.password_reset_data import PasswordResetData
from modules.password.managers.password_reset_manager import PasswordResetManager
from tests.integration.setup.config.config import get_config


class PasswordResetManagerFactoryTest(FactoryInterface):
    def invoke(self, service_manager):
        config = get_config()
        return PasswordResetManager(
            password_reset_data=service_manager.get(PasswordResetData.__name__),
            secret_key=config["SECRET_KEY"]
        )
