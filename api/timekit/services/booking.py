import json

import requests

from api.timekit.services.base import BaseService


class BookingService(BaseService):
    """
    This class is used to consume timekit APIs
    """

    def __init__(self):
        BaseService.__init__(self, "bookings")

    def get_booking(self, auth, booking_id=None, query_params=None):
        """
            This function is used to get the bookings
            :param auth: authentication parameters
            :param booking_id: booking id
            :param query_params: query string parameters
            :return: booking data in JSON format
            """
        try:
            booking_url = self.get_service_url()

            if booking_id:
                booking_url = booking_url + booking_id

            if query_params:
                booking_url = booking_url + "?" + query_params

            response = requests.get(booking_url,
                                    headers=self.get_header(),
                                    auth=auth)
            return self.get_response(response)
        except Exception as error:
            raise ValueError(error)

    def update_booking(self, auth, booking_id, action):
        """
            This function is used to update the booking state
            :param auth: authentication parameters
            :param booking_id: booking id
            :param action: booking action
            :return: booking data in JSON format
            """

        data = json.dumps({})
        try:
            booking_url = self.get_service_url() + booking_id + "/" + action
            response = requests.put(booking_url,
                                    headers=self.get_header(),
                                    auth=auth,
                                    data=data)
            return self.get_response(response)
        except Exception as error:
            raise ValueError(error)

