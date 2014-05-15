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
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from django_libs.loaders import load_member_from_setting
from django_libs.utils_email import send_email

from ...models import ObjectEvent, UserAggregationBase
from ... import app_settings


class Command(BaseCommand):
    """Class for the send_event_emails admin command."""
    def send_mail_to_user(self, email_context, to):
        """
        Function to send the digest to the user.

        First we check the preffered email of the User instance. You can
        add this function in your defined User Profile. Therefore check
        Django's AUTH_PROFILE_MODULE setting. If you haven't defined this
        function or defined a Profile module the email of the User instance is
        used.

        """
        email = to.email
        if (hasattr(to, 'get_profile')
                and hasattr(to.get_profile(), 'get_preferred_email')):
            email = to.get_profile().get_preferred_email()
        if email:
            send_email(
                '',
                {'event_types': email_context},
                'object_events/email/subject.html',
                'object_events/email/body.html',
                settings.FROM_EMAIL,
                [email],
            )
            self.sent_emails += 1

    def handle(self, interval='', **options):
        """Handles the send_event_emails admin command."""
        # Check if there is an aggregation class defined.
        start_of_command = timezone.now()
        if not interval in ('realtime', 'daily', 'weekly', 'monthly'):
            raise CommandError('Please provide a valid interval argument'
                               ' (realtime, daily, weekly, monthly)')
        aggregation = load_member_from_setting(
            'USER_AGGREGATION_CLASS', app_settings)()
        if not isinstance(aggregation, UserAggregationBase):
            raise CommandError(
                'Your user aggregation class must inherit UserAggregationBase')
        # Check interval argument and functions in the aggregation class.
        users = getattr(aggregation, 'get_users')(interval)
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
                self.send_mail_to_user(email_context, current_user)
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
            self.send_mail_to_user(email_context, current_user)
        print('The command took {0} seconds to finish. Sent {1} emails for {2}'
              ' events.'.format((timezone.now() - start_of_command).seconds,
                                self.sent_emails, object_events.count()))
