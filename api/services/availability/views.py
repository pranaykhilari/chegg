from django.db import IntegrityError
from django.db import transaction

from rest_framework import status
from rest_framework import views
from rest_framework.exceptions import ParseError

from api.models import UserAvailabilityFilter
from api.parser import parsers
from api.serializers.user_availability_filter_serializer import UserAvailabilityFilterSerializer
from common.util.utility import *
import logging
import json

logger = logging.getLogger(__name__)


class AvailabilityFilter(views.APIView):
    """
    This class consist of /availability/filters API's
    """
    parser_classes = (parsers.JSONSchemaParser,)
    schema = load_schema("availability.json")

    # constants
    FILTER_ID_KEY = "filter_id"

    def get(self, request, *args, **kwargs):
        """
        This function is used to handle the GET API's
        :param request: Request object
        :param args: arguments
        :param kwargs: URL parameters
        :return: HTTP Response
        """
        logger.info('retrieving details related to availability ...')
        try:
            user_id = get_user_id(request)
            app_user = get_user(user_id)

            filter_id = kwargs.get(self.FILTER_ID_KEY, None)

            if filter_id:
                filter_data = UserAvailabilityFilter.objects.get(id=filter_id)
                filter_data = UserAvailabilityFilterSerializer(filter_data).data
            else:
                filter_data_objects = UserAvailabilityFilter.objects.filter(user=app_user)
                filter_data = []
                for data in filter_data_objects:
                    filter_data.append(UserAvailabilityFilterSerializer(data).data)

            return Response(filter_data)
        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except (NotFound, UserAvailabilityFilter.DoesNotExist) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        """
        This function is used to handle the POST API's
        :param request: Request object
        :param args: arguments
        :param kwargs: URL parameters
        :return: HTTP Response
        """
        logger.info('Setting up availability ...')
        try:
            user_id = get_user_id(request)
            app_user = get_user(user_id)

            serializer = UserAvailabilityFilterSerializer(data=request.data)

            if serializer.is_valid():
                availability_filter = serializer.save(user=app_user)
                availability_filter_serializer = UserAvailabilityFilterSerializer(availability_filter)
                return Response(availability_filter_serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise ParseError(json.dumps(serializer.errors))

        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except (ParseError, IntegrityError) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        """
        This function is used to handle the PUT API's
        :param request: Request object
        :param args: arguments
        :param kwargs: URL parameters
        :return: HTTP Response
        """
        logger.info('Updating availability ...')
        try:
            filter_id = kwargs.get(self.FILTER_ID_KEY, None)
            user_id = get_user_id(request)

            with transaction.atomic():
                filter_data = UserAvailabilityFilter.objects.get(id=filter_id)
                serializer = UserAvailabilityFilterSerializer(filter_data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    raise ParseError(json.dumps(serializer.errors))
        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except (NotFound, UserAvailabilityFilter.DoesNotExist) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        """
        This function is used to handle the DELETE API's
        :param request: Request object
        :param args: arguments
        :param kwargs: URL parameters
        :return: HTTP Response
        """
        logger.info('Deleting availability ...')
        try:
            user_id = get_user_id(request)
            filter_id = kwargs.get(self.FILTER_ID_KEY, None)
            with transaction.atomic():
                filter_data = UserAvailabilityFilter.objects.get(id=filter_id)
                filter_data.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except (NotFound, IntegrityError, UserAvailabilityFilter.DoesNotExist) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_404_NOT_FOUND)
