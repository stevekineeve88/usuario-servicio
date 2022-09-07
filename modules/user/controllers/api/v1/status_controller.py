from http import HTTPStatus
from flask import Blueprint
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.user.exceptions.user_status_fetch_exception import UserStatusFetchException
from modules.user.managers.status_manager import StatusManager
from service_locator import get_service_manager

user_status_v1_api = Blueprint("user_status_v1_api", __name__)
ROOT = "/v1/status"


@user_status_v1_api.route(f"{ROOT}", methods=["GET"])
def get_all():
    """ GET user statuses
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    status_manager: StatusManager = service_locator.get(StatusManager.__name__)
    try:
        statuses = status_manager.get_all()
        return HTTPResponse(HTTPStatus.OK, "", statuses).get_response()
    except UserStatusFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
