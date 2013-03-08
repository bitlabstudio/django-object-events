"""Settings of the ``object_events``` application."""
from django.conf import settings


def get_user_aggregation_class():
    """This needs to be a lazy setting because of our tests."""
    return getattr(
        settings,
        'OBJECT_EVENTS_USER_AGGREGATION_CLASS',
        'object_events.models.UserAggregation',
    )

USER_AGGREGATION_CLASS = lambda: get_user_aggregation_class()
PAGINATION_ITEMS = getattr(settings, 'OBJECT_EVENTS_PAGINATION_ITEMS', 30)
