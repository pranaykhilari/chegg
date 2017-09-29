import logging
import urllib

from django.db import IntegrityError
from django.db import transaction
from rest_framework import status
from rest_framework import views
from rest_framework.exceptions import ParseError

from api.models import UserCalendar
from api.parser import parsers
from api.serializers.timekit.calendar_serializer import TimekitCalendarSerializer
from api.serializers.timekit.user_serializer import TimekitUserSerializer
from api.serializers.user_serializer import UserSerializer
from api.timekit.services.calendar import CalendarService
from api.timekit.services.user import UserService
from common.util.utility import *

logger = logging.getLogger(__name__)


class CalendarView(views.APIView):
    """
    This class consist of /calendars API's
    """
    parser_classes = (parsers.JSONSchemaParser,)
    schema = load_schema("calendar.json")

    # constants
    CALENDAR_ID_KEY = "calendar_id"

    def get(self, request, *args, **kwargs):
        """
        This function is used to handle the GET API's
        :param request: Request object
        :param args: arguments
        :param kwargs: URL parameters
        :return: HTTP Response
        """
        logger.info('retrieving calendar...')
        try:
            user_id = get_user_id(request)
            calendar_id = kwargs.get(self.CALENDAR_ID_KEY, None)
            query_params = None
            if request.GET:
                query_params = urllib.urlencode(request.GET)

            auth = get_user_auth(user_id)
            service = CalendarService()
            calendar_data = service.retrieve_calendar(auth, calendar_id, query_params)

            return Response(calendar_data)
        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except NotFound as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_404_NOT_FOUND)
        except (ParseError, ValueError) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """
        This function is used to handle the POST API's
        :param request: Request object
        :param args: arguments
        :param kwargs: URL parameters
        :return: HTTP Response
        """
        logger.info('Creating calendar...')
        try:
            user_id = get_user_id(request)

            with transaction.atomic():
                if User.objects.filter(chegg_uuid=user_id).exists():
                    user = User.objects.get(chegg_uuid=user_id)
                else:
                    timekit_user = TimekitUserSerializer(request.data)
                    data = json.dumps(timekit_user.data)
                    user_service = UserService()
                    user_data = user_service.create_user(data)
                    serializer = UserSerializer(user_data['data'])
                    user = serializer.create(serializer.data)
                    user.chegg_uuid = user_id
                    user.save()

                auth = user.dummy_email, user.token
                calendar_input = TimekitCalendarSerializer(request.data)
                calendar_input_data = json.dumps(calendar_input.data)
                calendar_service = CalendarService()
                calendar_data = calendar_service.create_calendar(auth, calendar_input_data)
                UserCalendar.objects.create(user=user, calendar_id=calendar_data['data']['id'])
                return Response(calendar_data, status=status.HTTP_201_CREATED)
        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except (ParseError, IntegrityError, ValueError) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        This function is used to handle the DELETE API's
        :param request: Request object
        :param args: arguments
        :param kwargs: URL parameters
        :return: HTTP Response
        """
        logger.info('Deleting calendar...')
        try:
            user_id = get_user_id(request)
            auth = get_user_auth(user_id)

            calendar_id = kwargs.get(self.CALENDAR_ID_KEY, None)
            with transaction.atomic():
                user_calendar = UserCalendar.objects.get(calendar_id=calendar_id)
                service = CalendarService()
                service.delete_calendar(auth, calendar_id)
                user_calendar.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except (NotFound, IntegrityError, UserCalendar.DoesNotExist) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_404_NOT_FOUND)
        except (ParseError, ValueError) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_400_BAD_REQUEST)
