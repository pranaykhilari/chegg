import json

from calendars.settings import local as settings
from rest_framework.exceptions import AuthenticationFailed, ParseError


class BaseService:
    """
    This is services base class
    """

    # constants
    SUCCESS_CODES = [200, 201]
    INVALID_CREDENTIALS = "Invalid credentials"
    BAD_REQUEST = "Bad request"
    SERVER_ERROR = "Internal server error"
    UNKNOWN_STATUS_CODE = "Unknown status code"

    def __init__(self, service_name):
        self.__service_name = service_name

    def get_header(self):
        """
        This function is used to get the header
        :return: header data
        """
        header = {'Timekit-App': settings.TIMEKIT_APP_NAME,
                  'content-type': 'application/json',
                  'Accept': 'text/plain'}
        return header

    def get_service_url(self):
        """
        This function is used to get the service url
        :return:
        """
        return settings.TIMEKIT_API_BASE_URL + "/" + self.__service_name + "/"

    def get_response(self, response):
        """
        This function is used to get the response according to response code
        :param response:
        :return: response or raise error
        """
        if response.status_code in self.SUCCESS_CODES:
            return response.json()
        elif response.status_code == 204:
            pass
        elif response.status_code == 401:
            raise AuthenticationFailed(self.INVALID_CREDENTIALS)
        elif response.status_code == 400:
            raise ParseError(self.BAD_REQUEST)
        elif response.status_code == 422:
            error = response.json()["errors"]
            raise ParseError(json.dumps(error))
        elif response.status_code == 500:
            raise ParseError(self.SERVER_ERROR)
        else:
            raise ParseError(self.UNKNOWN_STATUS_CODE)
