"""Models for the ``object_events`` app."""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import date
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


"""
Interval the user will be notified.

  realtime -> e.g. minute-by-minute
  daily    -> e.g. every day at midnight
  weekly   -> e.g. every sunday at 3 p.m.
  monthly  -> e.g. every last sunday of a month at 5 p.m.

You can change this dates in your settings and/or define your cronjobs.

"""
NOTIFICATION_INTERVALS = (
    ('realtime', _('realtime')),
    ('daily', _('daily')),
    ('weekly', _('weekly')),
    ('monthly', _('monthly')),
)


class ObjectEventType(models.Model):
    """
    Masterdata table containing event types.

    :title: Unique title of this event type. This will be used to decide which
      notification message to display or which partial to render.

    """
    title = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name=_('Title'),
        help_text=_('Please use a slugified name, e.g. "student-news".'),
    )

    def __unicode__(self):
        return self.title


class ObjectEvent(models.Model):
    """
    An event created by a user related to any object.

    :user: FK to the user who created this event. Leave this empty if this
      event was created by no user but automatically.
    :creation_date: Creation date of this event.
    :type: Type of this event.
    :email_sent: True, if user has received this event via email.
    :read_by_user: True, if user has noticed this event.
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

    email_sent = models.BooleanField(
        verbose_name=_('Has been sent in an email?'),
        default=False,
    )

    read_by_user = models.BooleanField(
        verbose_name=_('Has been noticed by the user?'),
        default=False,
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
    def create_event(user, content_object, event_content_object=None, type=''):
        """
        Creates an event for the given user, object and type.

        If the type doesn't exist, yet, it will be created, so make sure that
        you don't have any typos in your type title.

        :param user: The user who created this event.
        :param content_object: The object this event is attached to.
        :param event_content_object: The object that was created by this event.
        :type: String representing the type of this event.

        """
        type, created = ObjectEventType.objects.get_or_create(title=type)

        obj = ObjectEvent(user=user, content_object=content_object, type=type)
        if event_content_object is not None:
            obj.event_content_object = event_content_object
        obj.save()
        return obj

    def get_timesince(self):
        delta = (now() - self.creation_date)
        if delta.days <= 1:
            return '{0} ago'.format(timesince(self.creation_date, now()))
        if self.creation_date.year != now().year:
            return date(self.creation_date, 'd F Y')
        return date(self.creation_date, 'd F')


class ObjectEventSettingsManager(models.Manager):
    """Manager to return the one and only setting instance."""
    def get_settings(self, **kwargs):
        try:
            settings = self.get_query_set().get(pk=1)
        except ObjectEventSettings.DoesNotExist:
            return self.get_query_set().create(**kwargs)
        return settings

    def run_finished(self):
        settings = self.get_settings()
        settings.last_run = now()
        settings.save()
        return settings


class ObjectEventSettings(models.Model):
    """
    Table containing app-related settings and information.

    :last_run: Datetime of the last run of the management command
      ``send_event_emails``.

    """
    last_run = models.DateTimeField(
        verbose_name=_('Last run'),
        blank=True, null=True,
    )

    objects = ObjectEventSettingsManager()

    def save(self, **kwargs):
        if self.pk and self.pk == 1:
            return super(ObjectEventSettings, self).save(**kwargs)
        try:
            ObjectEventSettings.objects.get(pk=1)
        except ObjectEventSettings.DoesNotExist:
            return super(ObjectEventSettings, self).save(**kwargs)
        return False
