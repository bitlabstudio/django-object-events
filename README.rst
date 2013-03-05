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

Default: 'object_events.UserAggregation'

This is a class, which lets you create custom function to aggregate all users,
which should be notified. Therefore you can e.g. build a user profile, which
contains an interval or rrule setting.

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
OBJECT_EVENTS_USER_AGGREGATION above you will have to provide User querysets,
based on interval preferences. So create a custom model, which looks like the
one in our test app to use our basic aggregation class.


Roadmap
-------

See the issue tracker for current and upcoming features.
