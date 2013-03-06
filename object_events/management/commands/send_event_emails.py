"""
Custom admin command to send fresh object_events via email.

The interval is provided in an argument.
Options:
  realtime -> e.g. minute-by-minute
  daily    -> e.g. every day at midnight
  weekly   -> e.g. every sunday at 3 p.m.
  monthly  -> e.g. every last sunday of a month at 5 p.m.

The command always iterates over all events that have email_sent=False, but if
your app allows users to change their notification interval in their
UserProfile providing this parameter will call a different method on your
UserAggregation class implementation and therefore will include only a subset
of events (only for certain users).

"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_app
from django.utils import timezone

from django_libs.utils_email import send_email

from ...models import ObjectEvent
from ...object_events_settings import USER_AGGREGATION_CLASS


class Command(BaseCommand):
    """Class for the send_event_emails admin command."""
    def send_mail_to_user(self, email_context, to):
        """Function to send the digest to the user."""
        send_email(
            '',
            {'event_types': email_context},
            'object_events/email/subject.html',
            'object_events/email/body.html',
            'object_events/email/body_plain.html',
            from_email=settings.FROM_EMAIL,
            recipients=[to],
        )
        self.sent_emails += 1

    def handle(self, interval='', **options):
        """Handles the send_event_emails admin command."""
        # Check if there is an aggregation class defined.
        start_of_command = timezone.now()
        if not interval in ('realtime', 'daily', 'weekly', 'monthly'):
            raise CommandError('Please provide a valid interval argument'
                               ' (realtime, daily, weekly, monthly)')
        if not USER_AGGREGATION_CLASS:
            raise CommandError(
                'You need to set the OBJECT_EVENTS_USER_AGGREGATION class in'
                ' your project settings.')
        try:
            app, app_class = USER_AGGREGATION_CLASS.split('.')
        except ValueError:
            raise CommandError(
                'app_label and app_class should be separated by a dot in'
                ' the OBJECT_EVENTS_USER_AGGREGATION setting.')
        try:
            aggregation_app = get_app(app)
        except (ImportError, ImproperlyConfigured):
            raise CommandError('Unable to load defined app in the'
                               ' OBJECT_EVENTS_USER_AGGREGATION setting.')
        try:
            aggregation = aggregation_app.__getattribute__(app_class)
        except AttributeError:
            raise CommandError('Unable to load defined class in the'
                               ' OBJECT_EVENTS_USER_AGGREGATION setting.')
        # Check interval argument and functions in the aggregation class.
        try:
            users = getattr(aggregation(), 'get_users')(interval)
        except AttributeError:
            raise CommandError('Function get_users() not defined.')
        if not users:
            print('No users to send a {0} email.'.format(interval))
            return
        # Get all events , which hasn't been sent yet.
        object_events = ObjectEvent.objects.filter(
            email_sent=False, user__pk__in=users).order_by('user__pk')
        if not object_events:
            print('No events to send.')
            return
        email_context = {}
        current_user = None
        self.sent_emails = 0
        for object_event in object_events:
            if current_user != object_event.user and email_context:
                self.send_mail_to_user(email_context, current_user.email)
                email_context = {}
            current_user = object_event.user
            if email_context.get(object_event.event_type.title):
                email_context[object_event.event_type.title].append(
                    object_event)
            else:
                email_context.update({'{0}'.format(
                    object_event.event_type.title): [object_event]})
            object_event.email_sent = True
            object_event.save()
        # Send email even for the last user in the queryset, who cannot have
        # a follower
        if email_context:
            self.send_mail_to_user(email_context, current_user.email)
        print('The command took {0} seconds to finish. Sent {1} emails for {2}'
              ' events.'.format((timezone.now() - start_of_command).seconds,
                                self.sent_emails, object_events.count()))
