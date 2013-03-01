"""Dummy models to be used in test cases of the ``object_events`` app."""
from django.db import models


class DummyModel(models.Model):
    """Dummy model to be used in test cases of the ``object_events`` app."""
    name = models.CharField(max_length=256, blank=True)
