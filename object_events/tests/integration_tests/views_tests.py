"""Tests for views of the ``object_events``` application."""
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from ..factories import ObjectEventFactory
from ...models import ObjectEvent


class ObjectEventsListViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``ObjectEventsListView`` view."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()

    def get_view_name(self):
        return 'object_events_list'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.user)


class ObjectEventsMarkViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``ObjectEventsMarkView`` view."""
    longMessage = True

    def setUp(self):
        self.user = UserFactory()
        self.event = ObjectEventFactory(user=self.user)

    def get_view_name(self):
        return 'object_events_mark'

    def test_view(self):
        self.is_not_callable(user=self.user)
        self.is_callable(user=self.user, method='post',
                         and_redirects_to=reverse('object_events_list'))

        # ID is no integer
        self.is_not_callable(
            user=self.user, method='post', data={'single_mark': 'abc'})

        # ID is non-existant
        self.is_not_callable(
            user=self.user, method='post', data={'single_mark': 999})

        # Successful post
        self.is_callable(
            user=self.user, method='post', data={'single_mark': self.event.pk},
            and_redirects_to=reverse('object_events_list'))
        self.assertTrue(ObjectEvent.objects.get(pk=self.event.pk).read_by_user)
