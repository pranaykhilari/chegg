from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField


class User(models.Model):
    """
    Model class for calendar application User.
    This stores details related to user and which are used to communicate with Timekit.
    """

    # Correspond to Chegg user UUID
    chegg_uuid = models.CharField(max_length=255, db_index=True)

    # Stores api token received from Timekit.
    token = models.CharField(max_length=255)

    # Stores dummy email for the user received from Tutor's app
    dummy_email = models.EmailField()

    # Stores name of the third party calendar service application.
    source = models.CharField(max_length=255)

    # Timestamp when user created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp when user modified
    updated_at = models.DateTimeField(auto_now_add=True)


class UserCalendar(models.Model):
    """
    Model class to store the user calendars.
    This stores calendar Id received from Timekit.
    """

    # Foreign key for mapping it with user
    user = models.ForeignKey(User, related_name='calendar')

    # stores calendar_id received from Timekit.
    calendar_id = models.CharField(max_length=255)


class UserAvailabilityFilter(models.Model):
    """
    Model class to store the user availability filters.
    This is used in defining the availability slots on calendar.
    """

    # Foreign key for mapping it with user
    user = models.ForeignKey(User, related_name='availability')

    # Stores availability filter in json format.
    filters = JSONField()

    # Stores graph name (either 'instant' or 'confirm_decline')
    graph = models.CharField(max_length=255)

    # Stores details related to total duration of availability.
    future = models.CharField(max_length=255)

    # Stores duration for appointment.
    length = models.CharField(max_length=255)


class UserCalendarBooking(models.Model):
    """
    Model class for UserCalendarBooking
    Stores booking details received in Timekit webhooks.
    """

    # Foreign key reference for user
    user = models.ForeignKey(User, related_name='booking')

    # Stores details related to booking in json format.
    booking_data = JSONField()
