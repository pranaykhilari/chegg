from rest_framework import status
from rest_framework import views
from rest_framework.exceptions import ParseError

from api.timekit.services.booking import BookingService
from common.util.utility import *
import logging
import urllib

logger = logging.getLogger(__name__)

class BookingView(views.APIView):
    """
    This class consist of /bookings API's
    """

    # constants
    BOOKING_ID_KEY = "booking_id"
    ACTION_KEY = "action"

    def get(self, request, *args, **kwargs):
        """
        This function is used to handle the GET API's
        :param request: Request object
        :param args: arguments
        :param kwargs: URL parameters
        :return: HTTP Response
        """
        logger.info('retrieving details related to booking ...')
        try:
            booking_id = kwargs.get(self.BOOKING_ID_KEY, None)
            query_params = None
            query_params = urllib.urlencode(request.GET)

            user_id = get_user_id(request)
            auth = get_user_auth(user_id)

            service = BookingService()
            booking_data = service.get_booking(auth, booking_id, query_params)

            return Response(booking_data)
        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except NotFound as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_404_NOT_FOUND)
        except (ParseError, ValueError) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        This function is used to handle the PUT API's
        :param request: Request object
        :param args: arguments
        :param kwargs: URL parameters
        :return: HTTP Response
        """
        logger.info('Applying modifications related to booking ...')
        try:
            booking_id = kwargs.get(self.BOOKING_ID_KEY, None)
            action = kwargs.get(self.ACTION_KEY, None)
            user_id = get_user_id(request)
            auth = get_user_auth(user_id)
            service = BookingService()
            booking_data = service.update_booking(auth, booking_id, action)
            return Response(booking_data)
        except AuthenticationFailed as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_401_UNAUTHORIZED)
        except NotFound as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_404_NOT_FOUND)
        except (ParseError, ValueError) as error:
            logger.error(error)
            return get_error_response(error, status.HTTP_400_BAD_REQUEST)