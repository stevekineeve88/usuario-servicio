from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.auth.managers.refresh_token_manager import RefreshTokenManager
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager
from tests.integration.setup.integration_setup import IntegrationSetup


class RefreshTokenManagerTest(IntegrationSetup):
    refresh_token_manager: RefreshTokenManager = None
    user_manager: UserManager = None
    connection_manager: ConnectionManager = None
    status_manager: StatusManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.refresh_token_manager = cls.service_locator.get(RefreshTokenManager.__name__)
        cls.user_manager = cls.service_locator.get(UserManager.__name__)
        cls.status_manager = cls.service_locator.get(StatusManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)

    def test_create_creates_valid_refresh_token(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)

        refresh_token = self.refresh_token_manager.create(user.get_id(), user.get_uuid())
        payload = self.refresh_token_manager.verify_payload(refresh_token)
        self.assertEqual(payload["sub:id"], user.get_id())
        self.assertEqual(payload["sub:uuid"], user.get_uuid())

    def tearDown(self) -> None:
        result = self.connection_manager.query(
            "DELETE FROM user WHERE 1=1",
        )
        if not result.get_status():
            raise Exception(f"Failed to teardown refresh token test instance: {result.get_message()}")
