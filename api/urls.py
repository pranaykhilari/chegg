from django.conf.urls import url

from api.services.availability.views import AvailabilityFilter
from api.services.booking.views import BookingView
from api.services.calendar.views import CalendarView
from api.services.findtime.views import FindTime
from api.webhook.views import BookingWebhook

urlpatterns = [
    url(r'^calendars/(?P<calendar_id>[\w\.-]+)/$', CalendarView.as_view()),
    url(r'^calendars/$', CalendarView.as_view()),
    url(r'^bookings/(?P<booking_id>[\w\.-]+)/(?P<action>.+)/$', BookingView.as_view()),
    url(r'^bookings/$', BookingView.as_view()),
    url(r'^availability/filters/(?P<filter_id>[\w\.-]+)/$', AvailabilityFilter.as_view()),
    url(r'^availability/filters/$', AvailabilityFilter.as_view()),
    url(r'^findtime/$', FindTime.as_view()),
    url(r'^slug/bookings/$', BookingWebhook.as_view()),
]
