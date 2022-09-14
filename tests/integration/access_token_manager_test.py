from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.auth.managers.access_token_manager import AccessTokenManager
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager
from tests.integration.setup.integration_setup import IntegrationSetup


class AccessTokenManagerTest(IntegrationSetup):
    access_token_manager: AccessTokenManager = None
    user_manager: UserManager = None
    connection_manager: ConnectionManager = None
    status_manager: StatusManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.access_token_manager = cls.service_locator.get(AccessTokenManager.__name__)
        cls.user_manager = cls.service_locator.get(UserManager.__name__)
        cls.status_manager = cls.service_locator.get(StatusManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)

    def test_create_creates_access_token(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)

        token = self.access_token_manager.create(user)
        payload = self.access_token_manager.verify_payload(token)

        self.assertEqual(4, len(payload))
        self.assertEqual(user.get_id(), payload["sub:id"])
        self.assertEqual(user.get_uuid(), payload["sub:uuid"])
        self.assertEqual(user.get_email(), payload["sub:email"])

    def tearDown(self) -> None:
        result = self.connection_manager.query(f"""
            DELETE FROM user WHERE 1=1
        """)
        if not result.get_status():
            raise Exception(f"Failed to teardown access token manager test instance: {result.get_message()}")
