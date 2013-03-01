"""Models for the ``object_events`` app."""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import date
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class ObjectEventType(models.Model):
    """
    Masterdata table containing event types.

    :title: Unique title of this event type. This will be used to decide which
      notification message to display or which partial to render.

    """
    title = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_('Title'),
    )


class ObjectEvent(models.Model):
    """
    An event created by a user related to any object.

    :user: FK to the user who created this event. Leave this empty if this
      event was created by no user but automatically.
    :creation_date: Creation date of this event.
    :type: Type of this event.
    :content_object: Generic foreign key to the object this event is attached
      to. Leave this empty if it is a global event.
    :event_content_object: Generic foreign key to the object that has been
      created by this event. Leave this empty if the event did not create any
      object.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        related_name='events',
        null=True, blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    type = models.ForeignKey(
        ObjectEventType,
        verbose_name=_('Type'),
        related_name='events',
    )

    # Generic FK to the object this event is attached to
    content_type = models.ForeignKey(
        ContentType,
        related_name='event_content_objects',
        null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    # Generic FK to the object that got created by this event
    event_content_type = models.ForeignKey(
        ContentType,
        related_name='event_objects',
        null=True, blank=True
    )
    event_object_id = models.PositiveIntegerField(null=True, blank=True)
    event_content_object = generic.GenericForeignKey(
        'event_content_type', 'event_object_id')

    @staticmethod
    def create_event(user, content_object, event_content_object, type):
        """
        Creates an event for the given user, object and type.

        If the type doesn't exist, yet, it will be created, so make sure that
        you don't have any typos in your type title.

        :param user: The user who created this event.
        :param content_object: The object this event is attached to.
        :param event_content_object: The object that was created by this event.
        :type: String representing the type of this event.

        """
        try:
            type = ObjectEventType.objects.get(title=type)
        except ObjectEventType.DoesNotExist:
            type = ObjectEventType.objects.create(title=type)

        obj = ObjectEvent(user=user, content_object=content_object, type=type)
        if event_content_object is not None:
            obj.event_content_object = event_content_object
        obj.save()

    def get_timesince(self):
        delta = (now() - self.creation_date)
        if delta.days <= 1:
            return '{0} ago'.format(timesince(self.creation_date, now()))
        if self.creation_date.year != now().year:
            return date(self.creation_date, 'd F Y')
        return date(self.creation_date, 'd F')
