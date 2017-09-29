import requests

from api.timekit.services.base import BaseService


class FindtimeService(BaseService):
    """
    This class is used to consume timekit APIs
    """

    def __init__(self):
        BaseService.__init__(self, "findtime")

    def find_time(self, auth, data):
        """
            This function is used to find the mutual availability across users
            :param auth: authentication parameters
            :param data: Filter data in JSON format
            :return: available time slots data in JSON format
            """
        try:
            find_time_url = self.get_service_url()
            response = requests.post(find_time_url,
                                     headers=self.get_header(),
                                     data=data,
                                     auth=auth)
            return self.get_response(response)
        except Exception as error:
            raise ValueError(error)
