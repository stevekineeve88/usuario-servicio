import json
from http import HTTPStatus
from flask import Blueprint, request
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.user.exceptions.user_create_exception import UserCreateException
from modules.user.exceptions.user_delete_exception import UserDeleteException
from modules.user.exceptions.user_fetch_exception import UserFetchException
from modules.user.exceptions.user_status_fetch_exception import UserStatusFetchException
from modules.user.exceptions.user_update_exception import UserUpdateException
from modules.user.managers.status_manager import StatusManager
from modules.user.managers.user_manager import UserManager
from service_locator import get_service_manager

user_v1_api = Blueprint("user_v1_api", __name__)
ROOT = "/v1/user"


@user_v1_api.route(f"{ROOT}", methods=["POST"])
def create_user():
    """ POST user
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    user_manager: UserManager = service_locator.get(UserManager.__name__)
    status_manager: StatusManager = service_locator.get(StatusManager.__name__)
    try:
        data = json.loads(request.get_data().decode())
        user = user_manager.create(
            status_manager.get_by_const("ACTIVE"),
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"]
        )
        return HTTPResponse(HTTPStatus.CREATED, "", [user]).get_response()
    except UserCreateException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@user_v1_api.route(f"{ROOT}/<user_uuid>", methods=["PATCH"])
def update_user_by_uuid(user_uuid: str):
    """ PATCH user information
    Args:
        user_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    user_manager: UserManager = service_locator.get(UserManager.__name__)
    try:
        user = user_manager.get_by_uuid(user_uuid)

        data = json.loads(request.get_data().decode())
        user.set_first_name(data["first_name"] if "first_name" in data else user.get_first_name())
        user.set_last_name(data["last_name"] if "last_name" in data else user.get_last_name())

        new_user = user_manager.update(user)
        return HTTPResponse(HTTPStatus.OK, "", [new_user]).get_response()
    except UserFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except UserUpdateException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@user_v1_api.route(f"{ROOT}/<user_uuid>/status/<status_id>", methods=["PATCH"])
def update_user_status_by_user_uuid(user_uuid: str, status_id: int):
    """ PATCH user status
    Args:
        user_uuid (str):
        status_id (int):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    user_manager: UserManager = service_locator.get(UserManager.__name__)
    status_manager: StatusManager = service_locator.get(StatusManager.__name__)
    try:
        status = status_manager.get_by_id(int(status_id))
        user = user_manager.update_status(user_uuid, status)
        return HTTPResponse(HTTPStatus.OK, "", [user]).get_response()
    except UserUpdateException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except UserStatusFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except UserFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@user_v1_api.route(f"{ROOT}/<user_uuid>", methods=["GET"])
def get_user_by_uuid(user_uuid: str):
    """ GET user
    Args:
        user_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    user_manager: UserManager = service_locator.get(UserManager.__name__)
    try:
        user = user_manager.get_by_uuid(user_uuid)
        return HTTPResponse(HTTPStatus.OK, "", [user]).get_response()
    except UserFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@user_v1_api.route(f"{ROOT}", methods=["GET"])
def search_users():
    """ GET users
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    user_manager: UserManager = service_locator.get(UserManager.__name__)
    try:
        query_params = request.args.to_dict()
        search_query = query_params.get("search") or ""
        limit = query_params.get("limit") or 10
        offset = query_params.get("offset") or 0

        result = user_manager.search(search=search_query, limit=int(limit), offset=int(offset))
        http_response = HTTPResponse(HTTPStatus.OK, "", result.get_users())
        http_response.set_meta({
            "total_count": result.get_total_count(),
            "search": search_query,
            "limit": limit,
            "offset": offset
        })
        return http_response.get_response()
    except UserFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@user_v1_api.route(f"{ROOT}/<user_uuid>", methods=["DELETE"])
def delete_user_by_id(user_uuid: str):
    """ DELETE user
    Args:
        user_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    user_manager: UserManager = service_locator.get(UserManager.__name__)
    try:
        user_manager.delete(user_uuid)
        return HTTPResponse(HTTPStatus.OK, "").get_response()
    except UserDeleteException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
