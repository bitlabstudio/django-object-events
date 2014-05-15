Django Object Events
====================

Generic app for creating events that can be shown to the user in a
notifications list.

Think about Facebook. You got all kinds of events:

* User friends / unfriends user
* User posts a status update
* User likes something

All these things happen to a user and they happen on a certain object in the
database (his profile, a facebook page etc.).

If you wanted to create a timeline of events, you would have to query a ton
of different tables, then sort them via date, which would probably be near
impossible to solve via the Django ORM in a performant way.

With Django Object Events you can emit any kind of event and just drop it into
the ``object_event`` table. It has a foreign key to the afected user and
two more generic foreign keys: One for the object that caused the event and one
for the object that the event is about.

The object that caused the event could be another user writing a comment or
it could be a highscore entry reaching a certain value.

Accoring to the two examples above, the object that the event is about would be
the Comment object or the Highscore object respectively. This gives you the
chance to render a link to that object using it's ``get_absolute_url`` method.

Prerequisites
-------------

You need at least the following packages in your virtualenv:

* Django 1.4
* South
* Django Mailer


Installation
------------

To get the latest stable release from PyPi::

    $ pip install django-object-events

To get the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-object-events.git#egg=object_events

Add the app to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'object_events',
    ]

Run the south migrations to create the app's database tables::

    $ ./manage.py migrate object_events


Usage
-----

If you want to use this app without sending event notifications you don't have
to create settings or stuff. Simply use it, it's intuitive =)

Basically it's all about adding the right template tag::

    {% load object_events_tags %}
    {% render_notifications 3 %}

Then create some events. You might want to create a notification in your
views, your forms or via signals. An example::

    @receiver(comment_was_posted)
    def comment_was_posted_signal_handler(sender, comment, request, **kwargs):
        """Creates a notification for new comments."""
        ObjectEvent.create_event(
            user=comment.user, event_type='comment',
            content_object=comment,
            event_content_object=comment.content_object,
            additional_text=_('(Comment posted)'),
        )

Sending emails
++++++++++++++

For email support make sure to install ``django-mailer`` (see requirements.txt)

Make sure to add all email-related settings::

    ADMINS = (('YOUR_NAME', 'YOUR_EMAIL'), )
    FROM_EMAIL = ADMINS[0][1]

    MAILER_EMAIL_BACKEND = 'django_libs.test_email_backend.EmailBackend'
    TEST_EMAIL_BACKEND_RECIPIENTS = ADMINS

    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = FROM_EMAIL
    EMAIL_HOST_PASSWORD = "YOUR_PASSWORD"
    EMAIL_PORT = 587

    DEFAULT_FROM_EMAIL = FROM_EMAIL
    SERVER_EMAIL = FROM_EMAIL
    EMAIL_USE_TLS = True

Of course, change it to your email address and your email server settings.

Since the app is using intervals in sending email notifications we need to find
all users, which should retrieve fresh mail notifications. For that purpose
take a look at the setting ``OBJECT_EVENTS_USER_AGGREGATION_CLASS`` right
below.

Now, back to me. If you already created or are about to create a custom profile
model with a key to Django's User model and an interval field, which provides
these four options (realtime, daily, weekly, monthly), you can easily use our
predefined class ``object_events.models.UserAggregation``.

Use this profile as the general user profile (see setting AUTH_PROFILE_MODULE).

If you want to create your own aggregation class, make sure to inherit from
``object_events.models.UserAggregationBase``.

Now, call the management command manually or e.g. with cronjobs. Manually::

    ./manage.py send_event_emails realtime

With cronjobs for example:

.. code-block:: bash

    * * * * * $HOME/webapps/$DJANGO_APP_NAME/myproject/manage.py send_event_emails realtime > $HOME/mylogs/cron/send_event_emails.log 2>&1

Huh, cronjobs? If you are a bit server savvy connect to your server and type in
``EDITOR=nano crontab -e``.

Whatever, maybe you want to try it manually first.
Now you're free to work with this app, like, appending it to your project and
connect your models to it via post_save signals. Whatever you will do, have fun
with it!


Use with AJAX functions
+++++++++++++++++++++++

The basic functions like single_mark and bulk_mark can be easily used with
AJAX. Just add the following files to your base.html.

    <link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}object_events/css/object_events.css">
    <script type="text/javascript" src="{{ STATIC_URL }}object_events/js/object_events.js"></script>

The css and the js file are already imported in the objectevent_list.html
template.

Settings
--------

OBJECT_EVENTS_USER_AGGREGATION_CLASS
++++++++++++++++++++++++++++++++++++

Default: 'object_events.models.UserAggregation'

This is a class, which lets you create custom function to aggregate all users,
which should be notified. Therefore you can e.g. build a user profile, which
contains an interval or rrule setting.

Feel free to create custom functions and overrides. Just make sure to use the
base class ``object_events.models.UserAggregationBase``.

The following functions can be defined::

    get_realtime_users()
    get_daily_users()
    get_weekly_users()
    get_monthly_users()

Always return a list of primary keys of Django's User model.


AUTH_PROFILE_MODULE
++++++++++++++++++++++++++++++

Default: 'test_app.TestProfile'

You might know this setting already. This Django setting connects a custom
model to Django's User model. As you can see in the setting
OBJECT_EVENTS_USER_AGGREGATION_CLASS above you will have to provide User
querysets, based on interval preferences. So create a custom model, which looks
like the one in our test app to use our basic aggregation class.

If you want to provide different or custom email addresses to the email
notification command you can define a getter function called
``get_preferred_email``, e.g.:

    def get_preferred_email(self):
        if self.email:
            return self.email
        return self.user.email


OBJECT_EVENTS_PAGINATION_ITEMS
++++++++++++++++++++++++++++++

Default: 30

Amount of notifications to display in the notification list view.


Roadmap
-------

See the issue tracker for current and upcoming features.
