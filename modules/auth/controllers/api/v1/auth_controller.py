import json
from http import HTTPStatus
import jwt.exceptions
from flask import Blueprint, request
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.auth.exceptions.auth_password_exception import AuthPasswordException
from modules.auth.exceptions.auth_status_exception import AuthStatusException
from modules.auth.managers.access_token_manager import AccessTokenManager
from modules.auth.managers.auth_manager import AuthManager
from modules.user.exceptions.user_fetch_exception import UserFetchException
from service_locator import get_service_manager

auth_v1_api = Blueprint("auth_v1_api", __name__)
ROOT = "/v1/auth"


@auth_v1_api.route(f"{ROOT}", methods=["POST"])
def authentication():
    """ POST authentication
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    auth_manager: AuthManager = service_locator.get(AuthManager.__name__)
    try:
        data = json.loads(request.get_data().decode())
        validation_token = auth_manager.authenticate(data["email"], data["password"])
        return HTTPResponse(HTTPStatus.OK, "", [validation_token]).get_response()
    except (
        UserFetchException,
        AuthPasswordException,
        AuthStatusException
    ) as e:
        return HTTPResponse(HTTPStatus.FORBIDDEN, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@auth_v1_api.route(f"{ROOT}", methods=["GET"])
def verify_access_token():
    """ GET access token payload
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    access_token_manager: AccessTokenManager = service_locator.get(AccessTokenManager.__name__)
    try:
        headers = request.headers
        return {
            "data": [access_token_manager.verify_payload(headers.get("x-access-token"))]
        }, HTTPStatus.OK
    except (
        jwt.exceptions.InvalidSignatureError,
        jwt.exceptions.MissingRequiredClaimError
    ) as e:
        return HTTPResponse(HTTPStatus.FORBIDDEN, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@auth_v1_api.route(f"{ROOT}/refresh", methods=["GET"])
def refresh_access_token():
    """ GET new refresh and access token
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    auth_manager: AuthManager = service_locator.get(AuthManager.__name__)
    try:
        headers = request.headers
        validation_token = auth_manager.generate_validation_token(headers.get("x-refresh-token"))
        return HTTPResponse(HTTPStatus.OK, "", [validation_token]).get_response()
    except (
        jwt.exceptions.InvalidSignatureError,
        jwt.exceptions.MissingRequiredClaimError,
        UserFetchException,
        AuthStatusException
    ) as e:
        return HTTPResponse(HTTPStatus.FORBIDDEN, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
