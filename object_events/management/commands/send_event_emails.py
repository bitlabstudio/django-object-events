"""
Custom admin command to send fresh object_events via email.

The interval is provided in an argument.
Options:
  realtime -> e.g. minute-by-minute
  daily    -> e.g. every day at midnight
  weekly   -> e.g. every sunday at 3 p.m.
  monthly  -> e.g. every last sunday of a month at 5 p.m.

You can change this dates in your settings and/or define your cronjobs.

"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.db.models import get_app
from django.utils import timezone

from django_libs.utils_email import send_email

from ...models import ObjectEvent, ObjectEventSettings


class Command(BaseCommand):
    """Class for the send_event_emails admin command."""
    def send_mail_to_user(self, email_context, to):
        """Function to send the digest to the user."""
        send_email(
            '',
            {'types': email_context},
            'object_events/email/subject.html',
            'object_events/email/body.html',
            'object_events/email/body_plain.html',
            from_email=settings.FROM_EMAIL,
            recipients=[to],
        )

    def handle(self, *args, **options):
        """Handles the send_event_emails admin command."""
        # Check if there is an aggregation class defined.
        if not getattr(settings, 'OBJECT_EVENTS_USER_AGGREGATION', False):
            print('You need to set the OBJECT_EVENTS_USER_AGGREGATION class in'
                  ' your project settings.')
            return
        try:
            app, app_class = settings.OBJECT_EVENTS_USER_AGGREGATION.split('.')
        except ValueError:
            print('app_label and app_class should be separated by a dot in'
                  ' the OBJECT_EVENTS_USER_AGGREGATION setting.')
            return
        try:
            aggregation_app = get_app(app)
        except (ImportError, ImproperlyConfigured):
            print('Unable to load defined app in the'
                  ' OBJECT_EVENTS_USER_AGGREGATION setting.')
            return
        try:
            aggregation = aggregation_app.__getattribute__(app_class)
        except AttributeError:
            print('Unable to load defined class in the'
                  ' OBJECT_EVENTS_USER_AGGREGATION setting.')
            return
        # Check interval argument and functions in the aggregation class.
        if 'realtime' in args:
            try:
                users = aggregation().get_realtime_users()
            except AttributeError:
                print('Function get_realtime_users() not defined.')
                return
            object_event_settings = ObjectEventSettings.objects.get_settings()
            # If there's no last run registered, cover the last week.
            min_date = (object_event_settings.last_run
                        or timezone.now() - timezone.timedelta(days=7))
        elif 'daily' in args:
            try:
                users = aggregation().get_daily_users()
            except AttributeError:
                print('Function get_daily_users() not defined.')
                return
            min_date = timezone.now() - timezone.timedelta(
                days=settings.OBJECT_EVENTS_DAILY)
        elif 'weekly' in args:
            try:
                users = aggregation().get_weekly_users()
            except AttributeError:
                print('Function get_weekly_users() not defined.')
                return
            min_date = timezone.now() - timezone.timedelta(
                days=settings.OBJECT_EVENTS_WEEKLY)
        elif 'monthly' in args:
            try:
                users = aggregation().get_monthly_users()
            except AttributeError:
                print('Function get_monthly_users() not defined.')
                return
            now = timezone.now()
            min_date = timezone.datetime(
                now.year, now.month, settings.OBJECT_EVENTS_MONTHLY_DATE)
        else:
            print('Please provide a valid interval argument (realtime, daily,'
                  ' weekly, monthly)')
            return
        if not users:
            print('No users to send a mail.')
            return
        # Get all events from ``min_date`` till now.
        object_events = ObjectEvent.objects.filter(
            email_sent=False, creation_date__gt=min_date,
            user__pk__in=users).order_by('user__pk')
        if not object_events:
            print('No events to send.')
            return
        email_context = {}
        current_user = None
        for object_event in object_events:
            if current_user != object_event.user and email_context:
                self.send_mail_to_user(email_context, current_user.email)
                email_context = {}
            current_user = object_event.user
            if email_context.get(object_event.type.title):
                email_context[object_event.type.title].append(object_event)
            else:
                email_context.update({
                    '{0}'.format(object_event.type.title): [object_event],
                })
            object_event.email_sent = True
            object_event.save()
        # Send email even for the last user in the queryset, who cannot have
        # a follower
        self.send_mail_to_user(email_context, current_user.email)

        ObjectEventSettings.objects.run_finished()
        print('Send emails for {0} events.'.format(object_events.count()))
