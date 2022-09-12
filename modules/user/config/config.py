from typing import Dict
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface

from modules.user.data.factories.user_data_factory import UserDataFactory
from modules.user.data.status_data import StatusData
from modules.user.data.factories.status_data_factory import StatusDataFactory
from modules.user.data.user_data import UserData
from modules.user.managers.factories.status_manager_factory import StatusManagerFactory
from modules.user.managers.factories.user_manager_factory import UserManagerFactory
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager


class UserConfig:

    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            StatusManager.__name__: StatusManagerFactory(),
            UserManager.__name__: UserManagerFactory(),
            StatusData.__name__: StatusDataFactory(),
            UserData.__name__: UserDataFactory()
        }
