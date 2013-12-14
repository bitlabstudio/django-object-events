"""Factories of the ``object_events`` app."""
import factory

from django.utils.timezone import now

from django_libs.tests.factories import UserFactory

from ..models import ObjectEvent, ObjectEventType
from .test_app.models import DummyModel, TestProfile


class DummyModelFactory(factory.DjangoModelFactory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel

    name = 'Foobar'


class TestProfileFactory(factory.DjangoModelFactory):
    """Factory for the ``TestProfile`` model."""
    FACTORY_FOR = TestProfile

    user = factory.SubFactory(UserFactory)


class ObjectEventTypeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ObjectEventType

    title = factory.Sequence(lambda x: 'event_type{0}'.format(x))


class ObjectEventFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ObjectEvent

    user = factory.SubFactory(UserFactory)
    creation_date = factory.LazyAttribute(lambda x: now())
    event_type = factory.SubFactory(ObjectEventTypeFactory)
    content_object = factory.SubFactory(DummyModelFactory)
