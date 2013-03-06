"""Template tags for the ``object_events`` app."""
from django import template
from django.conf import settings

from ..models import ObjectEvent

register = template.Library()


@register.inclusion_tag('object_events/notifications.html', takes_context=True)
def render_notifications(context):
    """Template tag to render fresh notifications for the current user."""
    if context.get('request') and context['request'].user.is_authenticated():
        events = ObjectEvent.objects.filter(user=context['request'].user)
        if events:
            return {
                'authenticated': True,
                'unread_amount': events.filter(read_by_user=False).count(),
                'notifications': events[:settings.OBJECT_EVENTS_TAG_ITEMS],
            }
    return {}
