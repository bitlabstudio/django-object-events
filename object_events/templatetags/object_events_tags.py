"""Template tags for the ``object_events`` app."""
from django import template

from ..models import ObjectEvent

register = template.Library()


@register.simple_tag(takes_context=True)
def render_notifications(context, notification_amount=8, template_name=None):
    """Template tag to render fresh notifications for the current user."""
    ctx = {}
    if template_name is None:
        template_name = 'object_events/notifications.html'
    if context.get('request') and context['request'].user.is_authenticated():
        events = ObjectEvent.objects.filter(user=context['request'].user)
        ctx = {
            'authenticated': True,
            'request': context['request'],
            'unread_amount': events.filter(read_by_user=False).count(),
        }
        if events:
            ctx.update({'notifications': events[:notification_amount]})
    t = template.loader.get_template(template_name)
    return t.render(template.Context(ctx))
