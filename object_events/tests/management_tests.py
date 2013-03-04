"""Tests for the management commands of the ``object_events`` app."""
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from mailer.models import Message

from .factories import ObjectEventFactory, TestProfileFactory


class SendEventEmailsTestCase(TestCase):
    """Tests for the ``send_event_emails`` management command."""

    def test_general_imports_and_definitions(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = False
        self.assertFalse(call_command('send_event_emails'))

        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test'
        self.assertFalse(call_command('send_event_emails'))

        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test.Test'
        self.assertFalse(call_command('send_event_emails'))

        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test_app.Test'
        self.assertFalse(call_command('send_event_emails'))

        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test_app.EmptyAggregation'
        self.assertFalse(call_command('send_event_emails', 'realtime'))
        self.assertFalse(call_command('send_event_emails', 'daily'))
        self.assertFalse(call_command('send_event_emails', 'weekly'))
        self.assertFalse(call_command('send_event_emails', 'monthly'))

        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test_app.TestAggregation'
        self.assertFalse(call_command('send_event_emails'))

    def test_realtime(self):
        self.assertFalse(call_command('send_event_emails', 'realtime'))
        profile = TestProfileFactory(interval='realtime')
        self.assertFalse(call_command('send_event_emails', 'realtime'))
        first_object_event = ObjectEventFactory(user=profile.user)
        self.assertFalse(call_command('send_event_emails', 'realtime'))
        self.assertEqual(Message.objects.all().count(), 1)
        ObjectEventFactory(user=profile.user)
        ObjectEventFactory(user=profile.user, type=first_object_event.type)
        other_profile = TestProfileFactory(interval='realtime')
        ObjectEventFactory(user=other_profile.user)
        self.assertFalse(call_command('send_event_emails', 'realtime'))
        self.assertEqual(Message.objects.all().count(), 3)

    def test_daily(self):
        self.assertFalse(call_command('send_event_emails', 'daily'))
        profile = TestProfileFactory(interval='daily')
        self.assertFalse(call_command('send_event_emails', 'daily'))
        ObjectEventFactory(user=profile.user)
        self.assertFalse(call_command('send_event_emails', 'daily'))
        self.assertEqual(Message.objects.all().count(), 1)

    def test_weekly(self):
        self.assertFalse(call_command('send_event_emails', 'weekly'))
        profile = TestProfileFactory(interval='weekly')
        self.assertFalse(call_command('send_event_emails', 'weekly'))
        ObjectEventFactory(user=profile.user)
        self.assertFalse(call_command('send_event_emails', 'weekly'))
        self.assertEqual(Message.objects.all().count(), 1)

    def test_monthly(self):
        self.assertFalse(call_command('send_event_emails', 'monthly'))
        profile = TestProfileFactory(interval='monthly')
        self.assertFalse(call_command('send_event_emails', 'monthly'))
        ObjectEventFactory(user=profile.user)
        self.assertFalse(call_command('send_event_emails', 'monthly'))
        self.assertEqual(Message.objects.all().count(), 1)
