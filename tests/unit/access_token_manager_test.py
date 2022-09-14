import datetime
import time
import unittest
import jwt
from modules.auth.managers.access_token_manager import AccessTokenManager


class AccessTokenManagerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.secret_key = "some-random-key"
        self.access_token_manager: AccessTokenManager = AccessTokenManager(
            secret_key=self.secret_key
        )

    def test_verify_payload_fails_on_wrong_required_payload(self):
        token = jwt.encode({
            "wrong_param": 1,
            "sub:uuid": "SOME_UUID",
            "sub:email": "email@email.com",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=200)
        }, self.secret_key, algorithm="HS256")
        with self.assertRaises(jwt.exceptions.MissingRequiredClaimError):
            self.access_token_manager.verify_payload(token)
            self.fail("Did not fail on invalid access token payload")

    def test_verify_payload_fails_on_expired_signature(self):
        token = jwt.encode({
            "sub:id": 1,
            "sub:uuid": "SOME_UUID",
            "sub:email": "email@email.com",
            "exp": datetime.datetime.utcnow()
        }, self.secret_key, algorithm="HS256")
        time.sleep(2)
        with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
            self.access_token_manager.verify_payload(token)
            self.fail("Did not fail on refresh token expired signature")
