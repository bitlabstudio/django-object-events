"""Tests for tags of the ``object_events``` application."""
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.template.context import RequestContext
from django.test import TestCase
from django.test.client import RequestFactory

from django_libs.tests.factories import UserFactory

from ..templatetags.object_events_tags import render_notifications
from .factories import ObjectEventFactory


class RenderNotificationsTestCase(TestCase):
    """Tests for the ``render_notifications`` tag."""
    longMessage = True

    def test_tag(self):
        # create context mock
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        SessionMiddleware().process_request(request)
        request.session.save()
        context = RequestContext(request)

        # Returns empty dict if there is no authenticated user
        self.assertEqual(render_notifications(context), {})

        # If authenticated return an info
        request.user = UserFactory()
        self.assertEqual(render_notifications(context),
                         {'authenticated': True})

        # Returns notifications.html
        event = ObjectEventFactory(user=request.user)
        self.assertEqual(render_notifications(context).get('notifications'),
                         [event])
        self.assertEqual(render_notifications(context).get('unread_amount'), 1)
        self.assertEqual(render_notifications(context).get('authenticated'),
                         True)
