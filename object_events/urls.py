"""Urls for the ``object_events`` app."""
from django.conf.urls import patterns, url

from .views import ObjectEventsMarkView, ObjectEventsListView


urlpatterns = patterns(
    '',
    url(r'^mark/$', ObjectEventsMarkView.as_view(), name='object_events_mark'),
    url(r'^$', ObjectEventsListView.as_view(), name='object_events_list'),
)
