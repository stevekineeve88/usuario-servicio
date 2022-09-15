import datetime
import time
import unittest
from unittest.mock import patch, MagicMock
import jwt
from mysql_data_manager.modules.connection.objects.result import Result
from modules.password.data.password_reset_data import PasswordResetData
from modules.password.exceptions.password_reset_create_exception import PasswordResetCreateException
from modules.password.exceptions.password_reset_delete_exception import PasswordResetDeleteException
from modules.password.managers.password_reset_manager import PasswordResetManager


class PasswordResetManagerTest(unittest.TestCase):
    @patch("modules.password.data.password_reset_data.PasswordResetData")
    def setUp(self, password_reset_data: PasswordResetData) -> None:
        self.password_reset_data = password_reset_data
        self.secret_key = "some-random-key"
        self.password_reset_manager: PasswordResetManager = PasswordResetManager(
            password_reset_data=self.password_reset_data,
            secret_key=self.secret_key
        )

    def test_create_fails_on_delete_error(self):
        self.password_reset_data.delete_by_user_id = MagicMock(return_value=Result(False))
        self.password_reset_data.insert = MagicMock(return_value=Result(True))

        with self.assertRaises(PasswordResetDeleteException):
            self.password_reset_manager.create(1)
            self.fail("Did not fail deleting old password reset token")

        self.password_reset_data.delete_by_user_id.assert_called_once_with(1)
        self.password_reset_data.insert.assert_not_called()

    def test_create_fails_on_insert_error(self):
        self.password_reset_data.delete_by_user_id = MagicMock(return_value=Result(True))
        self.password_reset_data.insert = MagicMock(return_value=Result(False))

        with self.assertRaises(PasswordResetCreateException):
            self.password_reset_manager.create(1)
            self.fail("Did not fail creating new reset token")

        self.password_reset_data.delete_by_user_id.assert_called_once_with(1)
        self.password_reset_data.insert.assert_called_once()

    def test_verify_payload_fails_on_wrong_required_payload(self):
        token = jwt.encode({
            "wrong_param": 1,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }, self.secret_key, algorithm="HS256")
        with self.assertRaises(jwt.exceptions.MissingRequiredClaimError):
            self.password_reset_manager.verify_payload(token)
            self.fail("Did not fail on invalid password token payload")

    def test_verify_payload_fails_on_expired_signature(self):
        token = jwt.encode({
            "sub:id": 1,
            "exp": datetime.datetime.utcnow()
        }, self.secret_key, algorithm="HS256")
        time.sleep(2)
        with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
            self.password_reset_manager.verify_payload(token)
            self.fail("Did not fail on password token expired signature")
