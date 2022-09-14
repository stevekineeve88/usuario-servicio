import unittest
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_schema_manager.modules.migration.data.change_log_data import ChangeLogData
from mysql_schema_manager.modules.migration.data.migration_data import MigrationData
from mysql_schema_manager.modules.migration.managers.change_log_manager import ChangeLogManager
from mysql_schema_manager.modules.migration.managers.migration_manager import MigrationManager
from sk88_service_locator.modules.service.managers.service_manager import ServiceManager
from modules.auth.managers.access_token_manager import AccessTokenManager
from modules.auth.managers.refresh_token_manager import RefreshTokenManager
from service_locator import get_service_manager
from tests.integration.setup.factories.access_token_manager_factory_test import AccessTokenManagerFactoryTest
from tests.integration.setup.factories.connection_manager_factory_test import ConnectionManagerFactoryTest
from tests.integration.setup.factories.refresh_token_manager_factory_test import RefreshTokenManagerFactoryTest


class IntegrationSetup(unittest.TestCase):
    service_locator: ServiceManager = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.service_locator = get_service_manager()

        connection_manager_factory = ConnectionManagerFactoryTest()
        cls.service_locator.add({
            ConnectionManager.__name__: connection_manager_factory,
            RefreshTokenManager.__name__: RefreshTokenManagerFactoryTest(),
            AccessTokenManager.__name__: AccessTokenManagerFactoryTest()
        })

        migration_manager: MigrationManager = MigrationManager(
            migration_data=MigrationData(
                connection_manager=connection_manager_factory.get_connection_manager()
            ),
            change_log_manager=ChangeLogManager(
                change_log_data=ChangeLogData(
                    connection_manager=connection_manager_factory.get_connection_manager()
                )
            ),
            root_directory="."
        )
        migration_result = migration_manager.run()
        if not migration_result.get_status():
            raise Exception(migration_result.get_message())
