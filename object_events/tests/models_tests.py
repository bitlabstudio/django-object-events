"""Tests for the models of the ``object_events`` app."""
from django.test import TestCase

from .factories import ObjectEventFactory, ObjectEventTypeFactory


class ObjectEventTypeTestCase(TestCase):
    """Tests for the ``ObjectEventType`` model class."""
    def test_model(self):
        """Should be able to instantiate and save the model."""
        obj = ObjectEventTypeFactory()
        self.assertTrue(obj.pk)


class ObjectEventTestCase(TestCase):
    """Tests for the ``ObjectEvent`` model class."""
    def test_model(self):
        """Should be able to instantiate and save the model."""
        obj = ObjectEventFactory()
        self.assertTrue(obj.pk)
