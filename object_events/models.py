"""Models for the ``object_events`` app."""
from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable
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

For each interval that you allow in your app make sure that you define a
cronjob that is scheduled at this interval and called with the interval name
as it's parameter.

"""
NOTIFICATION_INTERVALS = (
    ('realtime', _('realtime')),
    ('daily', _('daily')),
    ('weekly', _('weekly')),
    ('monthly', _('monthly')),
)


class UserAggregationBase(object):
    """Base aggregation class to inherit from."""
    def get_users(self, interval):
        """Function to delegate user aggregation."""
        return getattr(self, 'get_{0}_users'.format(interval))()

    def get_realtime_users(self):
        """Function to aggregate users, which will be notified in realtime."""
        raise NotImplementedError()

    def get_daily_users(self):
        """Function to aggregate users, which will be notified daily."""
        raise NotImplementedError()

    def get_weekly_users(self):
        """Function to aggregate users, which will be notified weekly."""
        raise NotImplementedError()

    def get_monthly_users(self):
        """Function to aggregate users, which will be notified monthly."""
        raise NotImplementedError()


class UserAggregation(UserAggregationBase):
    """Class to aggregate 'realtime', 'daily', 'weekly', 'monthly' users."""
    def __init__(self):
        """Checks if there's a user profile."""
        if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
            raise SiteProfileNotAvailable(
                'You need to set AUTH_PROFILE_MODULE in your project settings')
        try:
            app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        except ValueError:
            raise SiteProfileNotAvailable(
                'app_label and model_name should be separated by a dot in'
                ' the AUTH_PROFILE_MODULE setting')
        self.model = models.get_model(app_label, model_name)
        if self.model is None:
            raise SiteProfileNotAvailable(
                'Unable to load the profile model, check'
                ' AUTH_PROFILE_MODULE in your project settings')
        if not hasattr(self.model(), 'interval'):
            raise SiteProfileNotAvailable('Model has no field "interval"')

    def get_realtime_users(self):
        """Function to aggregate users, which will be notified in realtime."""
        return self.model.objects.filter(interval='realtime').values_list(
            'user__pk', flat=True)

    def get_daily_users(self):
        """Function to aggregate users, which will be notified daily."""
        return self.model.objects.filter(interval='daily').values_list(
            'user__pk', flat=True)

    def get_weekly_users(self):
        """Function to aggregate users, which will be notified weekly."""
        return self.model.objects.filter(interval='weekly').values_list(
            'user__pk', flat=True)

    def get_monthly_users(self):
        """Function to aggregate users, which will be notified monthly."""
        return self.model.objects.filter(interval='monthly').values_list(
            'user__pk', flat=True)


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

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return u'{0}'.format(self.title)


class ObjectEvent(models.Model):
    """
    An event created by a user related to any object.

    :user: FK to the user who created this event. Leave this empty if this
      event was created by no user but automatically.
    :creation_date: Creation date of this event.
    :event_type: Type of this event.
    :email_sent: True, if user has received this event via email.
    :read_by_user: True, if user has noticed this event.
    :content_object: Generic foreign key to the object this event is attached
      to. Leave this empty if it is a global event.
    :event_content_object: Generic foreign key to the object that has been
      created by this event. Leave this empty if the event did not create any
      object.
    :additional_text: Plain text, which can be added to the notification,
      object, e.g. if you want to inform somebody that something has been
      deleted.

    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        related_name='object_events',
        null=True, blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    event_type = models.ForeignKey(
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

    additional_text = models.CharField(
        max_length=128,
        verbose_name=_('Additional text'),
        blank=True,
    )

    class Meta:
        ordering = ['-creation_date']

    @staticmethod
    def create_event(user, content_object, event_content_object=None,
                     event_type='', additional_text=''):
        """
        Creates an event for the given user, object and type.

        If the type doesn't exist, yet, it will be created, so make sure that
        you don't have any typos in your type title.

        :param user: The user who created this event.
        :param content_object: The object this event is attached to.
        :param event_content_object: The object that was created by this event.
        :event_type: String representing the type of this event.
        :additional_text: Additional text.

        """
        event_type_obj, created = ObjectEventType.objects.get_or_create(
            title=event_type)
        kwargs = {
            'user': user,
            'content_object': content_object,
            'event_type': event_type_obj,
            'additional_text': additional_text,
        }
        if event_content_object is not None:
            kwargs.update({'event_content_object': event_content_object})
        obj = ObjectEvent.objects.create(**kwargs)
        return obj

    def __unicode__(self):
        return u'{0}'.format(self.content_object)

    def get_timesince(self):
        delta = (now() - self.creation_date)
        if delta.days <= 1:
            return u'{} ago'.format(timesince(self.creation_date, now()))
        if self.creation_date.year != now().year:
            return date(self.creation_date, 'd F Y')
        return date(self.creation_date, 'd F')
