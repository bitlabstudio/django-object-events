"""Dummy models to be used in test cases of the ``object_events`` app."""
from django.db import models

from object_events.models import NOTIFICATION_INTERVALS


class DummyModel(models.Model):
    """Dummy model to be used in test cases of the ``object_events`` app."""
    name = models.CharField(max_length=256, blank=True)


class TestProfile(models.Model):
    """
    Enhanced ``User`` model to save and test notification intervals.

    :user: Reference to Django's User model.
    :interval: Setting to define the notification interval.

    """
    user = models.ForeignKey('auth.User')
    interval = models.CharField(max_length=20, choices=NOTIFICATION_INTERVALS)


class TestAggregation(object):
    """Class to aggregate 'realtime', 'daily', 'weekly', 'monthly' users."""
    def get_realtime_users(self):
        """Function to aggregate users, which will be notified in realtime."""
        return TestProfile.objects.filter(interval='realtime').values_list(
            'pk', flat=True)

    def get_daily_users(self):
        """Function to aggregate users, which will be notified daily."""
        return TestProfile.objects.filter(interval='daily').values_list(
            'pk', flat=True)

    def get_weekly_users(self):
        """Function to aggregate users, which will be notified weekly."""
        return TestProfile.objects.filter(interval='weekly').values_list(
            'pk', flat=True)

    def get_monthly_users(self):
        """Function to aggregate users, which will be notified monthly."""
        return TestProfile.objects.filter(interval='monthly').values_list(
            'pk', flat=True)


class EmptyAggregation(object):
    """Empty class to aggregate users."""
    pass
