from django.conf.urls import url

from widget import views
from widget.views import CalendarView

urlpatterns = [
    url(r'^calendar/(?P<jwt_token>[\w\.-]+)/(?P<user_id>\d+)/$', CalendarView.as_view()),
]