import re
from rest_framework import serializers
from api.models import UserAvailabilityFilter
from calendars.settings import local as settings


class UserAvailabilityFilterSerializer(serializers.Serializer):
    """
    UserAvailabilityFilter model serializer
    """
    id = serializers.ReadOnlyField()
    filters = serializers.JSONField()
    graph = serializers.CharField(default=settings.DEFAULT_AVAILABILITY_GRAPH)
    future = serializers.CharField(default=settings.DEFAULT_AVAILABILITY_FUTURE)
    length = serializers.CharField(default=settings.DEFAULT_AVAILABILITY_LENGTH)

    def create(self, validated_data):
        """
        Create and return a new `UserAvailabilityFilter` instance, given the validated data.
        """
        return UserAvailabilityFilter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update the UserAvailabilityFilter object
        :param instance:
        :param validated_data:
        :return:
        """
        instance.filters = validated_data.get("filters", instance.filters)
        instance.graph = validated_data.get("graph", instance.graph)
        instance.future = validated_data.get("future", instance.future)
        instance.length = validated_data.get("length", instance.length)
        instance.save()
        return instance

    def validate(self, data):
        """
        Validates the field value
        :param data:
        :return:
        """
        if data["graph"] in self.get_availability_graphs:
            return data
        else:
            raise serializers.ValidationError("Invalid graph value.")

    @property
    def get_availability_graphs(self):
        """
        This property is used to get the list of supported availability graphs
        :return: List of string of graphs
        """
        if settings.AVAILABILITY_GRAPHS:
            return re.sub(r'\s', '', settings.AVAILABILITY_GRAPHS).split(",")
        else:
            return [settings.DEFAULT_AVAILABILITY_GRAPH]
