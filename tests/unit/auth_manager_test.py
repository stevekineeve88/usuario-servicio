import datetime
import time
import unittest
from unittest.mock import patch, MagicMock
import jwt
from modules.auth.data.refresh_token_data import RefreshTokenData
from modules.auth.managers.access_token_manager import AccessTokenManager
from modules.auth.managers.auth_manager import AuthManager
from modules.auth.managers.refresh_token_manager import RefreshTokenManager
from modules.user.data.user_data import UserData
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager
from modules.user.objects.status import Status
from modules.user.objects.user import User
from modules.util.objects.redis_result import RedisResult


class AuthManagerTest(unittest.TestCase):

    @patch("modules.user.data.user_data.UserData")
    @patch("modules.user.managers.user_manager.UserManager")
    @patch("modules.user.managers.status_manager.StatusManager")
    @patch("modules.auth.data.refresh_token_data.RefreshTokenData")
    @patch("modules.auth.managers.access_token_manager.AccessTokenManager")
    def setUp(self,
              user_data: UserData,
              user_manager: UserManager,
              status_manager: StatusManager,
              refresh_token_data: RefreshTokenData,
              access_token_manager: AccessTokenManager
              ) -> None:
        self.user_data = user_data
        self.user_manager = user_manager
        self.status_manager = status_manager
        self.refresh_token_data = refresh_token_data
        self.access_token_manager = access_token_manager
        self.secret_key = "some-random-key"
        self.auth_manager: AuthManager = AuthManager(
            user_data=self.user_data,
            user_manager=self.user_manager,
            status_manager=self.status_manager,
            refresh_token_manager=RefreshTokenManager(
                refresh_token_data=self.refresh_token_data,
                secret_key=self.secret_key
            ),
            access_token_manager=self.access_token_manager
        )

    def test_generate_validation_token_fails_on_invalid_refresh_token(self):
        self.refresh_token_data.load_by_user_uuid = MagicMock(return_value=RedisResult(True))
        self.user_manager.get_by_id = MagicMock(return_value=User(Status(1, "CONST", "Description")))
        self.refresh_token_data.insert = MagicMock(return_value=RedisResult(True))
        self.access_token_manager.create = MagicMock(return_value="Some-Token")
        self.refresh_token_data.delete_by_user_uuid = MagicMock(return_value=RedisResult(True))
        token = jwt.encode({
            "sub:id": 1,
            "sub:uuid": "SOME_UUID",
            "exp": datetime.datetime.utcnow()
        }, self.secret_key, algorithm="HS256")
        time.sleep(2)
        with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
            self.auth_manager.generate_validation_token(token)
            self.fail("Did not fail to generate tokens with invalid refresh token")

        self.refresh_token_data.load_by_user_uuid.assert_not_called()
        self.user_manager.get_by_id.assert_not_called()
        self.refresh_token_data.insert.assert_not_called()
        self.access_token_manager.create.assert_not_called()
        self.refresh_token_data.delete_by_user_uuid.assert_not_called()
