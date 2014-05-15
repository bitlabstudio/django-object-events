"""Tests for the management commands of the ``object_events`` app."""
from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.management import call_command, CommandError
from django.test import TestCase
from django.test.utils import override_settings

from mailer.models import Message
from nose.tools import raises

from .factories import ObjectEventFactory, TestProfileFactory
from ..models import UserAggregation


class SendEventEmailsTestCase(TestCase):
    """Tests for the ``send_event_emails`` management command."""
    longMessage = True

    @raises(CommandError)
    def test_wrong_aggregation_class(self):
        with self.settings(
            OBJECT_EVENTS_USER_AGGREGATION_CLASS=('test_app.models.'
                                                  'EmptyAggregation')):
            call_command('send_event_emails', 'realtime')

    @raises(CommandError)
    def test_missing_argument(self):
        self.assertFalse(call_command('send_event_emails'))

    @raises(SiteProfileNotAvailable)
    @override_settings(AUTH_PROFILE_MODULE=False)
    def test_missing_user_profile(self):
        UserAggregation()

    @raises(SiteProfileNotAvailable)
    @override_settings(AUTH_PROFILE_MODULE='test')
    def test_wrong_user_profile_definition(self):
        UserAggregation()

    @raises(SiteProfileNotAvailable)
    @override_settings(AUTH_PROFILE_MODULE='test.Test')
    def test_wrong_user_profile_app(self):
        UserAggregation()

    @raises(SiteProfileNotAvailable)
    @override_settings(AUTH_PROFILE_MODULE='test_app.NonExistingProfile')
    def test_wrong_user_profile_model(self):
        UserAggregation()

    @raises(SiteProfileNotAvailable)
    @override_settings(AUTH_PROFILE_MODULE='test_app.WrongTestProfile')
    def test_user_profile_model_without_interval_field(self):
        UserAggregation()

    def test_realtime(self):
        self.assertFalse(call_command('send_event_emails', 'realtime'))
        profile = TestProfileFactory(interval='realtime')
        self.assertFalse(call_command('send_event_emails', 'realtime'))
        first_object_event = ObjectEventFactory(user=profile.user)
        self.assertFalse(call_command('send_event_emails', 'realtime'))
        self.assertEqual(Message.objects.all().count(), 1)
        ObjectEventFactory(user=profile.user)
        ObjectEventFactory(user=profile.user,
                           event_type=first_object_event.event_type)
        other_profile = TestProfileFactory(interval='realtime')
        ObjectEventFactory(user=other_profile.user,
                           event_type=first_object_event.event_type)
        ObjectEventFactory(user=other_profile.user,
                           event_type=first_object_event.event_type)
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
