import os
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.password.data.password_reset_data import PasswordResetData
from modules.password.managers.password_reset_manager import PasswordResetManager


class PasswordResetManagerFactory(FactoryInterface):
    """ Factory for creating password reset manager object
    """

    def invoke(self, service_manager):
        return PasswordResetManager(
            password_reset_data=service_manager.get(PasswordResetData.__name__),
            secret_key=os.environ["SECRET_KEY"]
        )
