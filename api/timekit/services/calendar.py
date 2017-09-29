import requests

from api.timekit.services.base import BaseService


class CalendarService(BaseService):
    """
    This class is used to consume timekit APIs
    """

    def __init__(self):
        BaseService.__init__(self, "calendars")

    def retrieve_calendar(self, auth, calendar_id=None, query_params=None):
        """
            This function is use to get the user calendars
            :param calendar_id: Calendar id
            :param query_params: query string parameters
            :param auth: authentication parameters
            :return: calendar data in JSON format
            """
        try:
            calendar_url = self.get_service_url()

            if calendar_id:
                calendar_url = calendar_url + calendar_id

            if query_params:
                calendar_url = calendar_url + "?" + query_params

            response = requests.get(calendar_url,
                                    headers=self.get_header(),
                                    auth=auth)
            return self.get_response(response)
        except Exception as error:
            raise ValueError(error)

    def create_calendar(self, auth, data):
        """
           This function is used to create the user calendar
           :param auth: authentication parameters
           :param data: Calendar data in JSON format
           :return: Calendar JSON object
           """
        try:
            calendar_url = self.get_service_url()
            response = requests.post(calendar_url,
                                     headers=self.get_header(),
                                     auth=auth,
                                     data=data)
            return self.get_response(response)
        except Exception as error:
            raise ValueError(error)

    def delete_calendar(self, auth, calendar_id):
        """
            This definition is used to delete the calendar from timekit
            :param auth: authentication parameters
            :param calendar_id: calendar id
            :return: nothing
            """
        try:
            calendar_url = self.get_service_url() + calendar_id
            response = requests.delete(calendar_url,
                                       headers=self.get_header(),
                                       auth=auth)
            return self.get_response(response)
        except Exception as error:
            raise ValueError(error)
