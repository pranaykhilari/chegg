from rest_framework import serializers

from api.models import User
from calendars.settings import local as settings


class UserSerializer(serializers.Serializer):
    """
    User model serializer
    """
    token = serializers.CharField(required=True, source="api_token")
    dummy_email = serializers.EmailField(source='email')
    source = serializers.CharField(allow_blank=False, default=settings.CALENDAR_SERVICE_SOURCE)

    def create(self, validated_data):
        """
        Creates new instance of User model
        :param validated_data:
        :return:
        """
        return User.objects.create(**validated_data)
