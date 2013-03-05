"""Tests for the models of the ``object_events`` app."""
from django.template.defaultfilters import date
from django.test import TestCase
from django.utils.timezone import now, timedelta

from django_libs.tests.factories import UserFactory

from ..models import ObjectEvent, ObjectEventType, ObjectEventSettings
from .factories import (
    ObjectEventFactory,
    ObjectEventTypeFactory,
    ObjectEventSettingsFactory,
)


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

    def test_create_event(self):
        user = UserFactory()
        content_object = UserFactory()
        event = ObjectEvent.create_event(user, content_object)
        self.assertIsInstance(event, ObjectEvent)
        self.assertEqual(ObjectEvent.objects.all().count(), 1)
        self.assertEqual(ObjectEventType.objects.all().count(), 1)

        # Test with a new content_object, created for this event
        event_content_object = UserFactory()
        event = ObjectEvent.create_event(user, content_object,
                                         event_content_object)
        self.assertEqual(event.event_content_object, event_content_object)

    def test_get_timesince(self):
        # Just created object_event
        object_event = ObjectEventFactory()
        self.assertEqual(object_event.get_timesince(), '0 minutes ago')

        # 'Young' object_event
        object_event.creation_date = now() - timedelta(days=1)
        self.assertEqual(object_event.get_timesince(), '1 day ago')

        # 'Teen' object_event
        object_event.creation_date = now() - timedelta(days=5)
        self.assertEqual(object_event.get_timesince(), date(
            object_event.creation_date, 'd F'))

        # 'Old' object_event
        object_event.creation_date = now() - timedelta(days=365)
        self.assertEqual(object_event.get_timesince(), date(
            object_event.creation_date, 'd F Y'))


class ObjectEventSettingsTestCase(TestCase):
    """Tests for the ``ObjectEventSettings`` model class."""
    def test_model(self):
        """Should be able to instantiate and save the model."""
        obj = ObjectEventSettingsFactory()
        self.assertTrue(obj.pk)

    def test_save(self):
        """Should allow only one instance."""
        obj = ObjectEventSettings()
        self.assertFalse(obj.pk)

        obj.save()
        self.assertTrue(obj.pk)
        self.assertEqual(ObjectEventSettings.objects.all().count(), 1)
        obj = ObjectEventSettings()
        obj.save()
        self.assertEqual(ObjectEventSettings.objects.all().count(), 1)
