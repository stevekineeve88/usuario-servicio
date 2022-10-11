import datetime
import time
import unittest
import jwt
from modules.auth.managers.refresh_token_manager import RefreshTokenManager


class RefreshTokenManagerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.secret_key = "some-random-key"
        self.refresh_token_manager: RefreshTokenManager = RefreshTokenManager(
            secret_key=self.secret_key
        )

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
