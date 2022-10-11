import time
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from modules.auth.exceptions.auth_password_exception import AuthPasswordException
from modules.auth.managers.auth_manager import AuthManager
from modules.password.exceptions.password_reset_fetch_exception import PasswordResetFetchException
from modules.password.managers.password_reset_manager import PasswordResetManager
from modules.user.exceptions.user_create_exception import UserCreateException
from modules.user.exceptions.user_delete_exception import UserDeleteException
from modules.user.exceptions.user_fetch_exception import UserFetchException
from modules.user.exceptions.user_update_exception import UserUpdateException
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager
from modules.user.objects.status import Status
from tests.integration.setup.integration_setup import IntegrationSetup


class UserManagerTest(IntegrationSetup):
    user_manager: UserManager = None
    connection_manager: ConnectionManager = None
    status_manager: StatusManager = None
    password_reset_manager: PasswordResetManager = None
    auth_manager: AuthManager = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_manager = cls.service_locator.get(UserManager.__name__)
        cls.connection_manager = cls.service_locator.get(ConnectionManager.__name__)
        cls.status_manager = cls.service_locator.get(StatusManager.__name__)
        cls.password_reset_manager = cls.service_locator.get(PasswordResetManager.__name__)
        cls.auth_manager = cls.service_locator.get(AuthManager.__name__)

    def test_create_creates_user(self):
        status = self.status_manager.get_by_const("ACTIVE")
        user_info = {
            "first_name": "Bob",
            "last_name": "Jenkins",
            "email": "bj@gmail.com",
            "password": "password1234"
        }
        expected_user = self.user_manager.create(status, **user_info)
        actual_user = self.user_manager.get_by_id(expected_user.get_id())

        self.assertEqual(expected_user.get_id(), actual_user.get_id())
        self.assertEqual(expected_user.get_uuid(), actual_user.get_uuid())
        self.assertEqual(expected_user.get_email(), actual_user.get_email())
        self.assertEqual(expected_user.get_first_name(), actual_user.get_first_name())
        self.assertEqual(expected_user.get_last_name(), actual_user.get_last_name())
        self.assertEqual(status.get_id(), actual_user.get_status().get_id())
        self.assertEqual(expected_user.get_created_timestamp(), actual_user.get_created_timestamp())
        self.assertEqual(expected_user.get_update_timestamp(), actual_user.get_update_timestamp())

    def test_create_fails_on_duplicate_email(self):
        status = self.status_manager.get_by_const("ACTIVE")
        user_info = {
            "first_name": "Bob",
            "last_name": "Jenkins",
            "email": "bj@gmail.com",
            "password": "password1234"
        }
        self.user_manager.create(status, **user_info)
        with self.assertRaises(UserCreateException):
            self.user_manager.create(status, **user_info)
            self.fail("Did not fail on create for duplicate user email")

    def test_create_fails_on_invalid_status(self):
        user_info = {
            "first_name": "Bob",
            "last_name": "Jenkins",
            "email": "bj@gmail.com",
            "password": "password1234"
        }
        with self.assertRaises(UserCreateException):
            self.user_manager.create(Status(123456, "INVALID_STATUS", "Description"), **user_info)
            self.fail("Did not fail on create for invalid status")

    def test_get_by_id_fails_on_invalid_id(self):
        with self.assertRaises(UserFetchException):
            self.user_manager.get_by_id(1)
            self.fail("Did not fail on fetch by invalid ID")

    def test_get_by_email_fetches_by_email(self):
        user_info = {
            "first_name": "Bob",
            "last_name": "Jenkins",
            "email": "bj@gmail.com",
            "password": "password1234"
        }
        status = self.status_manager.get_by_const("ACTIVE")
        user = self.user_manager.create(status, **user_info)
        fetched_user = self.user_manager.get_by_email(user.get_email())

        self.assertEqual(user.get_id(), fetched_user.get_id())
        self.assertEqual(user.get_email(), fetched_user.get_email())
        self.assertEqual(user.get_first_name(), fetched_user.get_first_name())
        self.assertEqual(user.get_last_name(), fetched_user.get_last_name())
        self.assertEqual(user.get_uuid(), fetched_user.get_uuid())
        self.assertEqual(user.get_created_timestamp(), fetched_user.get_created_timestamp())
        self.assertEqual(user.get_update_timestamp(), fetched_user.get_update_timestamp())
        self.assertEqual(user.get_status().get_id(), fetched_user.get_status().get_id())

    def test_get_by_email_fails_on_invalid_email(self):
        with self.assertRaises(UserFetchException):
            self.user_manager.get_by_email("random@gmail.com")
            self.fail("Did not fail on invalid email for fetching user")

    def test_update_updates_user(self):
        original_user_info = {
            "first_name": "Bob",
            "last_name": "Jenkins",
            "email": "bj@gmail.com",
            "password": "password1234"
        }

        new_user_info = {
            "first_name": "John",
            "last_name": "Hopkins"
        }

        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **original_user_info)

        time.sleep(3)
        user.set_first_name(new_user_info["first_name"])
        user.set_last_name(new_user_info["last_name"])
        new_user = self.user_manager.update(user)

        self.assertEqual(user.get_first_name(), new_user.get_first_name())
        self.assertEqual(user.get_last_name(), new_user.get_last_name())
        self.assertNotEqual(user.get_update_timestamp(), new_user.get_update_timestamp())

    def test_update_status_updates_status(self):
        old_status = self.status_manager.get_by_const("ACTIVE")
        new_status = self.status_manager.get_by_const("INACTIVE")

        user = self.user_manager.create(
            old_status,
            first_name="John",
            last_name="Jones",
            email="jj@gmail.com",
            password="password1234"
        )

        self.user_manager.update_status(user.get_uuid(), new_status)
        new_user = self.user_manager.get_by_id(user.get_id())

        self.assertEqual(new_status.get_id(), new_user.get_status().get_id())

    def test_update_status_fails_on_invalid_user_id(self):
        user = self.user_manager.create(
            self.status_manager.get_by_const("ACTIVE"),
            first_name="John",
            last_name="Jones",
            email="jj@gmail.com",
            password="password1234"
        )
        with self.assertRaises(UserFetchException):
            self.user_manager.update_status("sdfsdfsdf", self.status_manager.get_by_const("INACTIVE"))
            self.fail("Did not fail on update status for invalid user ID")

    def test_update_status_fails_on_invalid_status_id(self):
        user = self.user_manager.create(
            self.status_manager.get_by_const("ACTIVE"),
            first_name="John",
            last_name="Jones",
            email="jj@gmail.com",
            password="password1234"
        )
        with self.assertRaises(UserUpdateException):
            self.user_manager.update_status(user.get_uuid(), Status(123456, "SOME_CONST", "Description"))
            self.fail("Did not fail on update status for invalid status ID")

    def test_update_password_updates_password(self):
        old_password = "password1234"
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": old_password
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        password_reset_token = self.password_reset_manager.create(user.get_id())
        new_password = "new_password"
        self.user_manager.update_password(password_reset_token.get_token(), new_password)

        self.auth_manager.authenticate(user.get_email(), new_password)
        with self.assertRaises(AuthPasswordException):
            self.auth_manager.authenticate(user.get_email(), old_password)
            self.fail("Did not fail on authentication on old password before update")

    def test_update_password_allows_one_token_use(self):
        user_info = {
            "email": "ss@gmail.com",
            "first_name": "Scott",
            "last_name": "Smith",
            "password": "password1234"
        }
        user = self.user_manager.create(self.status_manager.get_by_const("ACTIVE"), **user_info)
        password_reset_token = self.password_reset_manager.create(user.get_id())

        self.user_manager.update_password(password_reset_token.get_token(), "some_new_password")
        with self.assertRaises(PasswordResetFetchException):
            self.user_manager.update_password(password_reset_token.get_token(), "another_new_password")
            self.fail("Did not fail on re-using password reset token for password update")

    def test_delete_deletes_user(self):
        user = self.user_manager.create(
            self.status_manager.get_by_const("ACTIVE"),
            first_name="John",
            last_name="Jones",
            email="jj@gmail.com",
            password="password1234"
        )
        self.user_manager.delete(user.get_uuid())

        with self.assertRaises(UserFetchException):
            self.user_manager.get_by_id(user.get_id())
            self.fail("Did not fail on missing deleted user")

    def test_delete_fails_on_invalid_id(self):
        with self.assertRaises(UserDeleteException):
            self.user_manager.delete("sfdsdf")
            self.fail("Did not fail on delete for invalid ID")

    def test_search_searches_users(self):
        active_status = self.status_manager.get_by_const("ACTIVE")
        self.user_manager.create(
            active_status,
            first_name="John",
            last_name="Benjamin",
            email="jb@gmail.com",
            password="password1234"
        )
        self.user_manager.create(
            active_status,
            first_name="John",
            last_name="Jones",
            email="jj@gmail.com",
            password="password1234"
        )
        self.user_manager.create(
            active_status,
            first_name="John",
            last_name="Reynold",
            email="jr@gmail.com",
            password="password1234"
        )

        user_result = self.user_manager.search(search="jones")

        self.assertEqual(1, len(user_result.get_users()))
        self.assertEqual(1, user_result.get_total_count())

    def test_search_paginates(self):
        active_status = self.status_manager.get_by_const("ACTIVE")
        self.user_manager.create(
            active_status,
            first_name="John",
            last_name="Benjamin",
            email="jb@gmail.com",
            password="password1234"
        )
        self.user_manager.create(
            active_status,
            first_name="John",
            last_name="Jones",
            email="jj@gmail.com",
            password="password1234"
        )
        self.user_manager.create(
            active_status,
            first_name="John",
            last_name="Reynold",
            email="jr@gmail.com",
            password="password1234"
        )

        user_result_1 = self.user_manager.search(search="john", limit=1, offset=0)
        user_result_2 = self.user_manager.search(search="john", limit=1, offset=1)

        self.assertEqual(1, len(user_result_1.get_users()))
        self.assertEqual(1, len(user_result_2.get_users()))

        self.assertEqual(3, user_result_1.get_total_count())
        self.assertEqual(3, user_result_2.get_total_count())

        self.assertEqual("Benjamin", user_result_1.get_users()[0].get_last_name())
        self.assertEqual("Jones", user_result_2.get_users()[0].get_last_name())

    def tearDown(self) -> None:
        result = self.connection_manager.query(f"""
            DELETE FROM user WHERE 1=1
        """)
        if not result.get_status():
            raise Exception(f"Failed to teardown user test instance: {result.get_message()}")
