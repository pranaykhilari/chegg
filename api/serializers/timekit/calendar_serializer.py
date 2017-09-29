from rest_framework import serializers


class TimekitCalendarSerializer(serializers.Serializer):
    """
    Timekit calendar object serializer
    """
    name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    description = serializers.CharField(required=True, allow_blank=False, max_length=255)
    backgroundcolor = serializers.CharField(required=False, allow_blank=True, max_length=255)
    foregroundcolor = serializers.CharField(required=False, allow_blank=True, max_length=255)
