"""Settings that need to be set in order to run the tests."""
import logging
import os

logging.getLogger("factory").setLevel(logging.WARN)

SECRET_KEY = 'foobar'

DEBUG = True

AUTH_USER_MODEL = 'auth.User'

SITE_ID = 1

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = 'object_events.tests.urls'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(__file__, '../../app_static/')

STATICFILES_DIRS = (
    os.path.join(__file__, 'test_static'),
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../templates'),
)

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), 'coverage')

COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
)


EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_nose',
    'mailer',
]

INTERNAL_APPS = [
    'object_events.tests.test_app',
    'object_events',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS


# email settings
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

# django setting to connect a model als a User profile
AUTH_PROFILE_MODULE = 'test_app.TestProfile'
