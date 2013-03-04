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

TODO (Aggregation Class, Cronjobs)


Settings
--------

OBJECT_EVENTS_USER_AGGREGATION
++++++++++++++++++++++++++++++

Default: 'test_app.TestAggregation'

This is a class, which lets you create custom function to aggregate all users,
which should be notified. Therefore you can e.g. build a user profile, which
contains an interval or rrule setting.

The following functions can be defined::

    get_realtime_users()
    get_daily_users()
    get_weekly_users()
    get_monthly_users()

Always return a list of primary keys of Django's User model.


OBJECT_EVENTS_REALTIME_MINUTES
++++++++++++++++++++++++++++++

Default: 2

The management command ``./manage.py send_event_emails realtime`` will process
object_events which are not older than ``2`` minutes.


OBJECT_EVENTS_DAILY
+++++++++++++++++++

Default: 1

The management command ``./manage.py send_event_emails daily`` will process
object_events which are not older than ``1`` day.


OBJECT_EVENTS_WEEKLY
++++++++++++++++++++

Default: 7

The management command ``./manage.py send_event_emails weekly`` will process
object_events which are not older than ``7`` days.


OBJECT_EVENTS_MONTHLY_DATE
++++++++++++++++++++++++++

Default: 1

The management command ``./manage.py send_event_emails monthly`` will process
object_events which are not older than the ``1st`` of the current month.


Roadmap
-------

See the issue tracker for current and upcoming features.
