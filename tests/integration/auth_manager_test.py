import time
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.auth.exceptions.auth_password_exception import AuthPasswordException
from modules.auth.exceptions.auth_status_exception import AuthStatusException
from modules.auth.managers.access_token_manager import AccessTokenManager
from modules.auth.managers.auth_manager import AuthManager
from modules.auth.managers.refresh_token_manager import RefreshTokenManager
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager
from tests.integration.setup.integration_setup import IntegrationSetup


class AuthManagerTest(IntegrationSetup):
    auth_manager: AuthManager = None
    user_manager: UserManager = None
    connection_manager: ConnectionManager = None
    status_manager: StatusManager = None
    access_token_manager: AccessTokenManager = None
    refresh_token_manager: RefreshTokenManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.auth_manager = cls.service_locator.get(AuthManager.__name__)
        cls.user_manager = cls.service_locator.get(UserManager.__name__)
        cls.status_manager = cls.service_locator.get(StatusManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)
        cls.refresh_token_manager = cls.service_locator.get(RefreshTokenManager.__name__)
        cls.access_token_manager = cls.service_locator.get(AccessTokenManager.__name__)

    def test_authenticate_authenticates_user(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        validation_token = self.auth_manager.authenticate(user_info["email"], user_info["password"])

        rt_payload = self.refresh_token_manager.verify_payload(validation_token.get_refresh_token())
        at_payload = self.access_token_manager.verify_payload(validation_token.get_access_token())
        self.assertEqual(user.get_id(), rt_payload["sub:id"])
        self.assertEqual(user.get_uuid(), rt_payload["sub:uuid"])
        self.assertEqual(user.get_id(), at_payload["sub:id"])
        self.assertEqual(user.get_uuid(), at_payload["sub:uuid"])
        self.assertEqual(user.get_email(), at_payload["sub:email"])

    def test_authenticate_fails_on_wrong_password(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        with self.assertRaises(AuthPasswordException):
            self.auth_manager.authenticate(user.get_email(), "WRONG_PASSWORD")
            self.fail("Did not fail on authenticating wrong password")

    def test_authenticate_fails_on_non_active_status(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("INACTIVE"), **user_info)
        with self.assertRaises(AuthStatusException):
            self.auth_manager.authenticate(user.get_email(), user_info["password"])
            self.fail("Did not fail on authenticating non active status")

    def test_generate_validation_token_generates_new_tokens(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        validation_token = self.auth_manager.authenticate(user_info["email"], user_info["password"])
        time.sleep(1)
        nv_token = self.auth_manager.generate_validation_token(validation_token.get_refresh_token())

        self.assertNotEqual(validation_token.get_refresh_token(), nv_token.get_refresh_token())
        self.assertNotEqual(validation_token.get_access_token(), nv_token.get_access_token())

    def test_generate_validation_token_fails_on_non_active_user_status(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        validation_token = self.auth_manager.authenticate(user_info["email"], user_info["password"])
        self.user_manager.update_status(user.get_uuid(), self.status_manager.get_by_const("INACTIVE"))
        with self.assertRaises(AuthStatusException):
            self.auth_manager.generate_validation_token(validation_token.get_refresh_token())
            self.fail("Did not fail on user status not active for token re generation")

    def tearDown(self) -> None:
        result = self.connection_manager.query(f"""
            DELETE FROM user WHERE 1=1
        """)
        if not result.get_status():
            raise Exception(f"Failed to teardown auth manager test instance: {result.get_message()}")
