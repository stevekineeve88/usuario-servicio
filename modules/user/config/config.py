from typing import Dict
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.user.data.status_data import StatusData
from modules.user.factories.data.status_data_factory import StatusDataFactory
from modules.user.factories.managers.status_manager_factory import StatusManagerFactory
from modules.user.managers.status_manager import StatusManager


class UserConfig:

    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            StatusManager.__name__: StatusManagerFactory(),
            StatusData.__name__: StatusDataFactory()
        }
