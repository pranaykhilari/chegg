import re

import jwt

from django.utils.deprecation import MiddlewareMixin
from calendars.settings import local as settings


def get_user_jwt(request):
    """
    JSON Web Token authentication. Inspects the token for the user_id.
    If not found then return None
    """
    user_id = None
    try:
        token = request.META['HTTP_AUTHORIZATION']
        token = re.sub(settings.JWT_AUTH_HEADER_PREFIX, '', token).strip()
        data = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = data['user_id']
    except:
        pass

    return user_id


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """ Middleware for authenticating JSON Web Tokens in Authorize Header """

    def process_request(self, request):
        request.user_id = get_user_jwt(request)
