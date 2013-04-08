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

    def get_preferred_email(self):
        return self.user.email


class WrongTestProfile(models.Model):
    """Wrong enhanced ``User`` model to test profile import."""
    pass


class EmptyAggregation(object):
    """Empty class to aggregate users."""
    pass
