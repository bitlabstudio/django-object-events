"""Template tags for the ``object_events`` app."""
from django import template

from ..models import ObjectEvent

register = template.Library()


@register.inclusion_tag('object_events/notifications.html', takes_context=True)
def render_notifications(context, notification_amount=8):
    """Template tag to render fresh notifications for the current user."""
    if context.get('request') and context['request'].user.is_authenticated():
        events = ObjectEvent.objects.filter(user=context['request'].user)
        if events:
            return {
                'authenticated': True,
                'request': context['request'],
                'unread_amount': events.filter(read_by_user=False).count(),
                'notifications': events[:notification_amount],
            }
        return {'authenticated': True}
    return {}
