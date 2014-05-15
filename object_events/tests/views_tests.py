"""Tests for views of the ``object_events``` application."""
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin

from .factories import ObjectEventFactory
from ..models import ObjectEvent


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
        self.is_callable(method='post',
                         and_redirects_to=reverse('object_events_list'))

        # ID is no integer
        self.is_not_callable(method='post', data={'single_mark': 'abc'})

        # ID is non-existant
        self.is_not_callable(method='post', data={'single_mark': 999})

        # Successful post and redirect to custom url
        self.is_callable(method='post', and_redirects_to='/test/',
                         data={'single_mark': self.event.pk, 'next': '/test/'})
        self.assertTrue(ObjectEvent.objects.get(pk=self.event.pk).read_by_user)

        # Succesful single-mark AJAX post
        resp = self.client.post(self.get_url(), {'single_mark': self.event.pk},
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.content, 'marked')

        # bulk_mark variable has no pk items
        self.is_callable(method='post', data={'bulk_mark': 'abc, x, []'},
                         and_redirects_to=reverse('object_events_list'))

        # bulk_mark variable is an empty string
        self.is_callable(method='post', data={'bulk_mark': ''},
                         and_redirects_to=reverse('object_events_list'))

        # Successful bulk_mark post
        e2 = ObjectEventFactory(user=self.user)
        e3 = ObjectEventFactory(user=self.user)
        self.is_callable(method='post',
                         data={'bulk_mark': '{0}, {1}, '.format(e2.pk, e3.pk)},
                         and_redirects_to=reverse('object_events_list'))
        self.assertTrue(ObjectEvent.objects.get(pk=e2.pk).read_by_user)
        self.assertTrue(ObjectEvent.objects.get(pk=e3.pk).read_by_user)

        # Succesful bulk-mark AJAX post
        resp = self.client.post(self.get_url(), {'bulk_mark': e2.pk},
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.content, 'marked')
