from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.auth.exceptions.refresh_token_delete_exception import RefreshTokenDeleteException
from modules.auth.exceptions.refresh_token_fetch_exception import RefreshTokenFetchException
from modules.auth.managers.refresh_token_manager import RefreshTokenManager
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager
from modules.util.managers.redis_manager import RedisManager
from tests.integration.setup.integration_setup import IntegrationSetup


class RefreshTokenManagerTest(IntegrationSetup):
    refresh_token_manager: RefreshTokenManager = None
    user_manager: UserManager = None
    connection_manager: ConnectionManager = None
    status_manager: StatusManager = None
    redis_manager: RedisManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.refresh_token_manager = cls.service_locator.get(RefreshTokenManager.__name__)
        cls.user_manager = cls.service_locator.get(UserManager.__name__)
        cls.status_manager = cls.service_locator.get(StatusManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)
        cls.redis_manager = cls.service_locator.get(RedisManager.__name__)

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

        fetch_refresh_token = self.refresh_token_manager.get_by_user_uuid(user.get_uuid())
        self.assertEqual(refresh_token, fetch_refresh_token)

    def test_get_by_user_uuid_fails_on_missing_user_uuid(self):
        with self.assertRaises(RefreshTokenFetchException):
            self.refresh_token_manager.get_by_user_uuid("SOME_RANDOM_TOKEN")
            self.fail("Did not fail on fetching invalid refresh token")

    def test_delete_by_user_uuid_deletes_valid_refresh_token(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)

        self.refresh_token_manager.create(user.get_id(), user.get_uuid())
        self.refresh_token_manager.delete_by_user_uuid(user.get_uuid())

        with self.assertRaises(RefreshTokenFetchException):
            self.refresh_token_manager.get_by_user_uuid(user.get_uuid())
            self.fail("Did not fail on retrieving refresh token after deletion")

    def test_delete_by_user_uuid_fails_on_missing_refresh_token(self):
        with self.assertRaises(RefreshTokenDeleteException):
            self.refresh_token_manager.delete_by_user_uuid("SOME_RANDOM_TOKEN")
            self.fail("Did not fail on deleting invalid token")

    def tearDown(self) -> None:
        result = self.connection_manager.query(
            "DELETE FROM user WHERE 1=1",
        )
        if not result.get_status():
            raise Exception(f"Failed to teardown refresh token test instance: {result.get_message()}")

        self.redis_manager.get_connection().flushdb()
