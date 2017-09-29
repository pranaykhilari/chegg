from rest_framework import serializers


class TimekitUserSerializer(serializers.Serializer):
    """
    Timekit user object serializer
    """
    email = serializers.EmailField(source='dummy_email')
    timezone = serializers.CharField(required=True, allow_blank=False, max_length=255)
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=255)
