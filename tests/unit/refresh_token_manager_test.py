import datetime
import time
import unittest
from unittest.mock import patch, MagicMock
import jwt
from modules.auth.data.refresh_token_data import RefreshTokenData
from modules.auth.exceptions.refresh_token_create_exception import RefreshTokenCreateException
from modules.auth.exceptions.refresh_token_delete_exception import RefreshTokenDeleteException
from modules.auth.managers.refresh_token_manager import RefreshTokenManager
from modules.util.objects.redis_result import RedisResult


class RefreshTokenManagerTest(unittest.TestCase):

    @patch("modules.auth.data.refresh_token_data.RefreshTokenData")
    def setUp(self, refresh_token_data: RefreshTokenData) -> None:
        self.refresh_token_data = refresh_token_data
        self.secret_key = "some-random-key"
        self.refresh_token_manager: RefreshTokenManager = RefreshTokenManager(
            refresh_token_data=self.refresh_token_data,
            secret_key=self.secret_key
        )

    def test_create_fails_on_create_error(self):
        self.refresh_token_data.insert = MagicMock(return_value=RedisResult(False))
        with self.assertRaises(RefreshTokenCreateException):
            self.refresh_token_manager.create(1, "UUID")
            self.fail("Did not fail on refresh token creation")
        self.refresh_token_data.insert.assert_called_once()

    def test_verify_payload_fails_on_wrong_required_payload(self):
        token = jwt.encode({
            "wrong_param": 1,
            "sub:uuid": "SOME_UUID",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=200)
        }, self.secret_key, algorithm="HS256")
        with self.assertRaises(jwt.exceptions.MissingRequiredClaimError):
            self.refresh_token_manager.verify_payload(token)
            self.fail("Did not fail on invalid refresh token payload")

    def test_verify_payload_fails_on_expired_signature(self):
        token = jwt.encode({
            "sub:id": 1,
            "sub:uuid": "SOME_UUID",
            "exp": datetime.datetime.utcnow()
        }, self.secret_key, algorithm="HS256")
        time.sleep(2)
        with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
            self.refresh_token_manager.verify_payload(token)
            self.fail("Did not fail on refresh token expired signature")
            
    def test_delete_by_user_id_fails_on_failed_delete(self):
        self.refresh_token_data.delete_by_user_uuid = MagicMock(return_value=RedisResult(False))
        with self.assertRaises(RefreshTokenDeleteException):
            self.refresh_token_manager.delete_by_user_uuid("some-random-uuid")
            self.fail("Did not fail on deleting refresh token by user ID")

        self.refresh_token_data.delete_by_user_uuid.assert_called_once_with("some-random-uuid")
