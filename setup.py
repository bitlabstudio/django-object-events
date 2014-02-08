import os
from setuptools import setup, find_packages
import object_events as app


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-object-events",
    version=app.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, reusable, events, notifications, generic',
    author='Martin Brochhaus',
    author_email='mbrochh@gmail.com',
    url="https://github.com/bitmazk/django-object-events",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django_libs>=1.42.3',
    ]
)
