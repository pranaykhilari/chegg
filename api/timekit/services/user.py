import requests

from api.timekit.services.base import BaseService


class UserService(BaseService):
    """
    This class is used to consume timekit APIs
    """

    def __init__(self):
        BaseService.__init__(self, "users")

    def create_user(self, data):
        """
            This function is used to create the user on timekit
            :param data: This is JSON data which contains user information
            :return: User JSON object
            """
        try:
            user_url = self.get_service_url()
            response = requests.post(user_url,
                                     headers=self.get_header(),
                                     data=data)
            return self.get_response(response)
        except Exception as error:
            raise ValueError(error)