from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.user.data.status_data import StatusData
from modules.user.managers.status_manager import StatusManager


class StatusManagerFactory(FactoryInterface):
    """ Factory for creating status manager object
    """

    def invoke(self, service_manager):
        return StatusManager(
            status_data=service_manager.get(StatusData.__name__)
        )
