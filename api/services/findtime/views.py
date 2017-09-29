import json

from rest_framework import status
from rest_framework import views
from rest_framework.exceptions import ParseError

from api.parser import parsers
from api.timekit.services.findtime import FindtimeService

from common.util.utility import *
import logging

logger = logging.getLogger(__name__)


class FindTime(views.APIView):
    """
    This class consist of /findtime API's
    """
    parser_classes = (parsers.JSONSchemaParser,)
    schema = load_schema("findtime.json")

    def post(self, request, *args, **kwargs):
        """
        This function is used to find the time slots based on conditions
        :param request: Request object
        :param args: arguments
        :param kwargs: parameters
        :return: Response object
        """
        logger.info('Checking availability ...')
        try:
            user_id = get_user_id(request)
            auth = get_user_auth(user_id)
            # implicitly calls parser_classes
            data = json.dumps(request.data)
            service = FindtimeService()
            slots = service.find_time(auth, data)
            return Response(slots)
        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except NotFound as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_404_NOT_FOUND)
        except (ParseError, ValueError) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_400_BAD_REQUEST)
