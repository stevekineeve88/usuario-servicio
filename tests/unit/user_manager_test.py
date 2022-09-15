import unittest
from unittest.mock import patch, MagicMock
from mysql_data_manager.modules.connection.objects.result import Result
from modules.password.exceptions.password_reset_match_exception import PasswordResetMatchException
from modules.password.managers.password_reset_manager import PasswordResetManager
from modules.password.objects.password_reset_token import PasswordResetToken
from modules.user.data.user_data import UserData
from modules.user.exceptions.user_update_exception import UserUpdateException
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager


class UserManagerTest(unittest.TestCase):

    @patch("modules.user.data.user_data.UserData")
    @patch("modules.user.managers.status_manager.StatusManager")
    @patch("modules.password.managers.password_reset_manager.PasswordResetManager")
    def setUp(
            self,
            user_data: UserData,
            status_manager: StatusManager,
            password_reset_manager: PasswordResetManager
    ) -> None:
        self.user_data = user_data
        self.status_manager = status_manager
        self.password_reset_manager = password_reset_manager
        self.user_manager: UserManager = UserManager(
            user_data=self.user_data,
            status_manager=self.status_manager,
            password_reset_manager=self.password_reset_manager
        )

    def test_update_password_fails_on_token_mismatch(self):
        user_id = 1
        self.password_reset_manager.verify_payload = MagicMock(return_value={
            "sub:id": user_id,
            "exp": 123432
        })
        self.password_reset_manager.get_by_token = MagicMock(return_value=PasswordResetToken(1, "WRONG", user_id))
        self.password_reset_manager.delete_by_user_id = MagicMock()
        self.user_data.update_password = MagicMock(return_value=Result(True))

        correct_token = "RIGHT"
        with self.assertRaises(PasswordResetMatchException):
            self.user_manager.update_password(correct_token, "new_password")
            self.fail("Did not fail on mismatching tokens for updating password")

        self.password_reset_manager.verify_payload.assert_called_once_with(correct_token)
        self.password_reset_manager.get_by_token.assert_called_once_with(correct_token)
        self.password_reset_manager.delete_by_user_id.assert_called_once_with(user_id)
        self.user_data.update_password.assert_not_called()

    def test_update_password_fails_on_update_error(self):
        user_id = 1
        correct_token = "RIGHT"

        self.password_reset_manager.verify_payload = MagicMock(return_value={
            "sub:id": user_id,
            "exp": 123432
        })
        self.password_reset_manager.get_by_token = MagicMock(return_value=PasswordResetToken(1, correct_token, user_id))
        self.password_reset_manager.delete_by_user_id = MagicMock()
        self.user_data.update_password = MagicMock(return_value=Result(False))
        with self.assertRaises(UserUpdateException):
            self.user_manager.update_password(correct_token, "new_password")
            self.fail("Did not fail on update error for updating password")

        self.password_reset_manager.verify_payload.assert_called_once_with(correct_token)
        self.password_reset_manager.get_by_token.assert_called_once_with(correct_token)
        self.password_reset_manager.delete_by_user_id.assert_called_once_with(user_id)
        self.user_data.update_password.assert_called_once()

    def test_search_defaults_limit_if_over_100(self):
        self.user_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 101,
            "offset": 0
        }

        self.user_manager.search(**params)
        self.user_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_limit_if_under_0(self):
        self.user_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": -1,
            "offset": 0
        }

        self.user_manager.search(**params)
        self.user_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_offset_if_under_0(self):
        self.user_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 20,
            "offset": -1
        }

        self.user_manager.search(**params)
        self.user_data.search.assert_called_once_with(
            search=params["search"],
            limit=params["limit"],
            offset=0
        )
