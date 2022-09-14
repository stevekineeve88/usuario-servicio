import datetime
from typing import Dict
import jwt
from modules.auth.data.refresh_token_data import RefreshTokenData
from modules.auth.exceptions.refresh_token_create_exception import RefreshTokenCreateException
from modules.auth.exceptions.refresh_token_delete_exception import RefreshTokenDeleteException
from modules.auth.exceptions.refresh_token_fetch_exception import RefreshTokenFetchException
from modules.auth.objects.refresh_token import RefreshToken
from modules.user.objects.user import User


class RefreshTokenManager:
    def __init__(self, **kwargs):
        self.__refresh_token_data: RefreshTokenData = kwargs.get("refresh_token_data")
        self.__secret_key: str = kwargs.get("secret_key")

    def create(self, user: User) -> RefreshToken:
        token = jwt.encode({
            "sub:id": user.get_id(),
            "sub:uuid": user.get_uuid(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=200)
        }, self.__secret_key, algorithm="HS256")
        result = self.__refresh_token_data.insert(user.get_id(), token)
        if not result.get_status():
            raise RefreshTokenCreateException("Could not create refresh token")
        return self.get(token)

    def get(self, token: str) -> RefreshToken:
        result = self.__refresh_token_data.load_by_token(token)
        if result.get_affected_rows() == 0:
            raise RefreshTokenFetchException("Could not find refresh token")
        return self.__build_refresh_token(result.get_data()[0])

    def delete(self, token: str):
        result = self.__refresh_token_data.delete_by_token(token)
        if result.get_affected_rows() == 0:
            raise RefreshTokenDeleteException("Could not delete refresh token")

    def verify_payload(self, token: str) -> Dict[str, any]:
        return jwt.decode(token, self.__secret_key, algorithms=["HS256"], options={
            "require": [
                "sub:id",
                "sub:uuid",
                "exp"
            ]
        })

    @classmethod
    def __build_refresh_token(cls, data: Dict[str, any]) -> RefreshToken:
        return RefreshToken(
            id=data["id"],
            token=data["token"],
            user_id=data["user_id"],
            created_timestamp=data["created_timestamp"]
        )
