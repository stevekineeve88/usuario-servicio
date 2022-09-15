import json
from http import HTTPStatus
import jwt.exceptions
from flask import Blueprint, request
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.password.exceptions.password_reset_create_exception import PasswordResetCreateException
from modules.password.exceptions.password_reset_delete_exception import PasswordResetDeleteException
from modules.password.exceptions.password_reset_fetch_exception import PasswordResetFetchException
from modules.password.exceptions.password_reset_match_exception import PasswordResetMatchException
from modules.password.managers.password_reset_manager import PasswordResetManager
from modules.user.exceptions.user_fetch_exception import UserFetchException
from modules.user.exceptions.user_update_exception import UserUpdateException
from modules.user.managers.user_manager import UserManager
from service_locator import get_service_manager

password_v1_api = Blueprint("password_v1_api", __name__)
ROOT = "/v1/password/reset"


@password_v1_api.route(f"{ROOT}", methods=["POST"])
def create_password_reset_token():
    """ POST password reset token
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    password_reset_manager: PasswordResetManager = service_locator.get(PasswordResetManager.__name__)
    user_manager: UserManager = service_locator.get(UserManager.__name__)
    try:
        data = json.loads(request.get_data().decode())
        user = user_manager.get_by_email(data["email"])
        password_reset_token = password_reset_manager.create(user.get_id())
        return HTTPResponse(HTTPStatus.CREATED, "", [password_reset_token]).get_response()
    except UserFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except (
        PasswordResetDeleteException,
        PasswordResetCreateException
    ) as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@password_v1_api.route(f"{ROOT}", methods=["GET"])
def verify_password_reset_token():
    """ GET password reset token payload
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    password_reset_manager: PasswordResetManager = service_locator.get(PasswordResetManager.__name__)
    try:
        headers = request.headers
        return {
            "data": [password_reset_manager.verify_payload(headers.get("x-password-reset-token"))]
        }, HTTPStatus.OK
    except (
        jwt.exceptions.InvalidSignatureError,
        jwt.exceptions.MissingRequiredClaimError
    ) as e:
        return HTTPResponse(HTTPStatus.FORBIDDEN, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@password_v1_api.route(f"{ROOT}", methods=["PATCH"])
def update_user_password():
    """ PATCH user password
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    user_manager: UserManager = service_locator.get(UserManager.__name__)
    try:
        headers = request.headers
        data = json.loads(request.get_data().decode())

        user_manager.update_password(headers.get("x-password-reset-token"), data["password"])
        return HTTPResponse(HTTPStatus.OK, "").get_response()
    except UserUpdateException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except (
        jwt.exceptions.InvalidSignatureError,
        jwt.exceptions.MissingRequiredClaimError,
        PasswordResetFetchException,
        PasswordResetDeleteException,
        PasswordResetMatchException,
    ) as e:
        return HTTPResponse(HTTPStatus.FORBIDDEN, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
