"""Tests for the management commands of the ``object_events`` app."""
from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.management import call_command
from django.test import TestCase

from mailer.models import Message
from nose.tools import raises

from .factories import ObjectEventFactory, TestProfileFactory
from ..models import UserAggregation


class SendEventEmailsTestCase(TestCase):
    """Tests for the ``send_event_emails`` management command."""
    longMessage = True

    def setUp(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = ('object_events.'
                                                   'UserAggregation')
        settings.AUTH_PROFILE_MODULE = 'test_app.TestProfile'

    @raises(SystemExit)
    def test_missing_aggregation_class(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = False
        self.assertFalse(call_command('send_event_emails', 'realtime'))

    @raises(SystemExit)
    def test_wrong_aggregation_definition(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test'
        self.assertFalse(call_command('send_event_emails', 'realtime'))

    @raises(SystemExit)
    def test_wrong_aggregation_app(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test.Test'
        self.assertFalse(call_command('send_event_emails', 'realtime'))

    @raises(SystemExit)
    def test_wrong_aggregation_class(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test_app.Test'
        self.assertFalse(call_command('send_event_emails', 'realtime'))

    @raises(SystemExit)
    def test_missing_aggregation_function_realtime(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test_app.EmptyAggregation'
        self.assertFalse(call_command('send_event_emails', 'realtime'))

    @raises(SystemExit)
    def test_missing_aggregation_function_daily(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test_app.EmptyAggregation'
        self.assertFalse(call_command('send_event_emails', 'daily'))

    @raises(SystemExit)
    def test_missing_aggregation_function_weekly(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test_app.EmptyAggregation'
        self.assertFalse(call_command('send_event_emails', 'weekly'))

    @raises(SystemExit)
    def test_missing_aggregation_function_monthly(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = 'test_app.EmptyAggregation'
        self.assertFalse(call_command('send_event_emails', 'monthly'))

    @raises(SystemExit)
    def test_missing_argument(self):
        settings.OBJECT_EVENTS_USER_AGGREGATION = ('object_events.'
                                                   'UserAggregation')
        self.assertFalse(call_command('send_event_emails'))

    @raises(SiteProfileNotAvailable)
    def test_missing_user_profile(self):
        settings.AUTH_PROFILE_MODULE = False
        UserAggregation()

    @raises(SiteProfileNotAvailable)
    def test_wrong_user_profile_definition(self):
        settings.AUTH_PROFILE_MODULE = 'test'
        UserAggregation()

    @raises(SiteProfileNotAvailable)
    def test_wrong_user_profile_app(self):
        settings.AUTH_PROFILE_MODULE = 'test.Test'
        UserAggregation()

    @raises(SiteProfileNotAvailable)
    def test_wrong_user_profile_model(self):
        settings.AUTH_PROFILE_MODULE = 'test_app.NonExistingProfile'
        UserAggregation()

    @raises(SiteProfileNotAvailable)
    def test_user_profile_model_without_interval_field(self):
        settings.AUTH_PROFILE_MODULE = 'test_app.WrongTestProfile'
        UserAggregation()

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
        ObjectEventFactory(user=other_profile.user,
                           type=first_object_event.type)
        ObjectEventFactory(user=other_profile.user,
                           type=first_object_event.type)
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
