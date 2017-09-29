import json
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework import views

from api.models import UserCalendarBooking, UserCalendar
from common.util.utility import *
import logging

logger = logging.getLogger(__name__)


class BookingWebhook(views.APIView):
    """
    This class is use to process callback data received from Timekit
    """
    # constants
    TENTATIVE = "tentative"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    CANCELLED = "cancelled"
    ERROR = "error"
    COMPLETED = "completed"
    CALENDAR = "calendar"
    ID = "id"
    STATE = "state"

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """
        This function is called when Timekit send data on slug/bookings/ webhook URL
        :param request: request
        :param args: arguments
        :param kwargs: parameters
        :return: Success response
        """

        try:
            booking_json = json.loads(request.body)
            state = booking_json[self.STATE]

            logger.debug("received data in webhook")

            if self.TENTATIVE == state:
                BookingCallbackHandler.tentative_callback_handler(booking_json)
            elif self.CONFIRMED == state:
                BookingCallbackHandler.confirmed_callback_handler(booking_json)
            elif self.DECLINED == state:
                BookingCallbackHandler.declined_callback_handler(booking_json)
            elif self.CANCELLED == state:
                BookingCallbackHandler.cancelled_callback_handler(booking_json)
            elif self.ERROR == state:
                BookingCallbackHandler.error_callback_handler(booking_json)
            elif self.COMPLETED == state:
                BookingCallbackHandler.completed_callback_handler(booking_json)

            calendar_id = booking_json[self.CALENDAR][self.ID]
            user = UserCalendar.objects.get(calendar_id=calendar_id).user
            calendar_booking = UserCalendarBooking.objects.create(user=user, booking_data=booking_json)
            calendar_booking.save()

            return Response(status=status.HTTP_200_OK)
        except UserCalendar.DoesNotExist as error:
            logger.error(error)
            Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            Response(status=status.HTTP_404_NOT_FOUND)


class BookingCallbackHandler:
    """
    This class is used as a callback handler in webhooks
    """

    def __init__(self):
        pass

    @staticmethod
    def tentative_callback_handler(booking_data):
        """
        This is callback handler for tentative booking state
        :param booking_data:
        :return:
        """
        pass

    @staticmethod
    def confirmed_callback_handler(booking_data):
        """
        This is callback handler for confirmed booking state
        :param booking_data:
        :return:
        """
        pass

    @staticmethod
    def declined_callback_handler(booking_data):
        """
        This is callback handler for declined booking state
        :param booking_data:
        :return:
        """
        pass

    @staticmethod
    def cancelled_callback_handler(booking_data):
        """
        This is callback handler for cancelled booking state
        :param booking_data:
        :return:
        """
        pass

    @staticmethod
    def error_callback_handler(booking_data):
        """
        This is callback handler for error booking state
        :param booking_data:
        :return:
        """
        pass

    @staticmethod
    def completed_callback_handler(booking_data):
        """
        This is callback handler for completed booking state
        :param booking_data:
        :return:
        """
        pass
