import json

import re

import jwt
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import View
from jwt import DecodeError

from rest_framework.exceptions import AuthenticationFailed

from api.models import User, UserCalendar, UserAvailabilityFilter
from calendars.settings import local as settings


class CalendarView(View):
    # constants
    CALENDAR_ID_KEY = "calendar_id"
    FILTER_ID_KEY = "filter_id"
    FILTERS_KEY = "filters"

    def get(self, request, jwt_token, user_id):
        """This function is use to display calendar for the particular user. This request accept optionally calendar id,
        filter id and extra parameters. Calendar id and filter id are used to display specific calendar for specific
        filter. If calendar id and filter id is not provided then this function will take latest values for them.
        Extra parameters are passed to timekit customer which will be retrieve in future for further use.
        """
        try:
            token = re.sub(settings.JWT_AUTH_HEADER_PREFIX, '', jwt_token).strip()
            data = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

            calendar_id = None
            filter_id = None
            customer_parameter = {}
            if request.GET:
                for key, value in request.GET.iteritems():
                    if key == self.CALENDAR_ID_KEY:
                        calendar_id = value
                    elif key == self.FILTER_ID_KEY:
                        filter_id = value
                    else:
                        customer_parameter.update({key: value})

            user = User.objects.get(chegg_uuid=user_id)

            if calendar_id:
                calendar = UserCalendar.objects.get(calendar_id=calendar_id)
            else:
                calendar = UserCalendar.objects.filter(user_id=user).last()

            if filter_id:
                availability_filter = UserAvailabilityFilter.objects.get(id=filter_id)
            else:
                availability_filter = UserAvailabilityFilter.objects.filter(user_id=user).last()

            filters = availability_filter.filters

            return render(request, 'calendar.html', {
                'user': user,
                'calendar': calendar,
                'filters': json.dumps(filters),
                'availability_filter': availability_filter,
                'app_name': settings.TIMEKIT_APP_NAME,
                'customer_parameter': json.dumps(customer_parameter)
            })
        except DecodeError as error:
            return HttpResponseNotFound("Invalid TOKEN")
        except User.DoesNotExist as error:
            return HttpResponseNotFound(error)
        except UserCalendar.DoesNotExist as error:
            return HttpResponseNotFound(error)
        except UserAvailabilityFilter.DoesNotExist as error:
            return HttpResponseNotFound(error)
