import time
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.auth.managers.auth_manager import AuthManager
from modules.password.exceptions.password_reset_delete_exception import PasswordResetDeleteException
from modules.password.exceptions.password_reset_fetch_exception import PasswordResetFetchException
from modules.password.managers.password_reset_manager import PasswordResetManager
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager
from modules.util.managers.redis_manager import RedisManager
from tests.integration.setup.integration_setup import IntegrationSetup


class PasswordResetManagerTest(IntegrationSetup):
    auth_manager: AuthManager = None
    user_manager: UserManager = None
    connection_manager: ConnectionManager = None
    redis_manager: RedisManager = None
    status_manager: StatusManager = None
    password_reset_manager: PasswordResetManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.auth_manager = cls.service_locator.get(AuthManager.__name__)
        cls.user_manager = cls.service_locator.get(UserManager.__name__)
        cls.status_manager = cls.service_locator.get(StatusManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)
        cls.redis_manager = cls.service_locator.get(RedisManager.__name__)
        cls.password_reset_manager = cls.service_locator.get(PasswordResetManager.__name__)

    def test_create_creates_password_reset_token(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        password_reset_token = self.password_reset_manager.create(user.get_id())
        fetched_token = self.password_reset_manager.get_by_token(password_reset_token.get_token())

        self.assertEqual(password_reset_token.get_id(), fetched_token.get_id())
        self.assertEqual(password_reset_token.get_token(), fetched_token.get_token())
        self.assertEqual(password_reset_token.get_user_id(), fetched_token.get_user_id())

    def test_create_creates_one_token_per_user(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        prt_1 = self.password_reset_manager.create(user.get_id())
        time.sleep(1)
        prt_2 = self.password_reset_manager.create(user.get_id())

        with self.assertRaises(PasswordResetFetchException):
            self.password_reset_manager.get_by_token(prt_1.get_token())
            self.fail("Did not fail on fetch password token for new creation")

        fetched_token = self.password_reset_manager.get_by_token(prt_2.get_token())
        self.assertEqual(prt_2.get_id(), fetched_token.get_id())
        self.assertEqual(prt_2.get_user_id(), fetched_token.get_user_id())

    def test_get_by_token_fails_on_missing_token(self):
        with self.assertRaises(PasswordResetFetchException):
            self.password_reset_manager.get_by_token("RANDOM_TOKEN")
            self.fail("Did not fail on missing password token")

    def test_delete_by_user_id_deletes_token(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        password_reset_token = self.password_reset_manager.create(user.get_id())
        self.password_reset_manager.delete_by_user_id(user.get_id())

        with self.assertRaises(PasswordResetFetchException):
            self.password_reset_manager.get_by_token(password_reset_token.get_token())
            self.fail("Did not fail on fetch password token after deletion")

    def test_delete_by_user_id_fails_on_missing_user(self):
        with self.assertRaises(PasswordResetDeleteException):
            self.password_reset_manager.delete_by_user_id(1)
            self.fail("Did not fail on delete password token for invalid user ID")

    def test_verify_payload_verifies_payload(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        password_reset_token = self.password_reset_manager.create(user.get_id())

        payload = self.password_reset_manager.verify_payload(password_reset_token.get_token())
        self.assertEqual(password_reset_token.get_user_id(), payload["sub:id"])

    def tearDown(self) -> None:
        result = self.connection_manager.query(
            "DELETE FROM user WHERE 1=1",
        )
        if not result.get_status():
            raise Exception(f"Failed to teardown password reset test instance: {result.get_message()}")

        self.redis_manager.get_connection().flushdb()
