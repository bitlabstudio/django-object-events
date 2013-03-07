"""Settings of the ``object_events``` application."""
from django.conf import settings


USER_AGGREGATION_CLASS = getattr(
    settings,
    'OBJECT_EVENTS_USER_AGGREGATION_CLASS',
    'object_events.models.UserAggregation',
)
PAGINATION_ITEMS = getattr(settings, 'OBJECT_EVENTS_PAGINATION_ITEMS', 30)
