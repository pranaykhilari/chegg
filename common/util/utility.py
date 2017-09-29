import json

from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response

from api.models import User
from calendars.settings import local as settings

LOGGING = settings.LOGGING
import logging

logger = logging.getLogger(__name__)

# JSON schema directory path
JSON_SCHEMA_DIR = "api/parser/schema/"


def get_error_response(error, status_code):
    """
    This function is used to get the formatted error response
    :param error: Error object
    :param status_code: HTTP status code
    :return: Response object
    """
    logger.error(error)
    return Response(
        {'error': format(error)},
        status=status_code
    )


def get_user(user_id):
    """
    This function is used to get calendar app user using user id
    :param user_id: app user id
    :return: AppUser object
    """
    try:
        app_user = User.objects.get(chegg_uuid=user_id)
        return app_user
    except User.DoesNotExist:
        logger.error("Resource does not exist")
        raise NotFound("Resource does not exist")


def get_user_auth(user_id):
    """
    This function is used to get the user authentication parameters
    :param user_id: String
    :return: authentication tuple
    """
    app_user = get_user(user_id)
    return app_user.dummy_email, app_user.token


def load_schema(schema_file_name):
    """
    This function is used to load the json schema from file.
    :param schema_file_name: schema file name
    :return: JSON object
    """
    try:
        schema = JSON_SCHEMA_DIR + schema_file_name
        return json.loads(open(schema).read())
    except IOError as error:
        raise


def get_user_id(request):
    """
    Get the user id from request object if it is None then raise the Authentication exception
    :param request: request object
    :return: user id
    """
    if request.user_id:
        return request.user_id
    else:
        raise AuthenticationFailed("Invalid TOKEN")
