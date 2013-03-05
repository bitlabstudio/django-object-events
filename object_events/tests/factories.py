"""Factories of the ``object_events`` app."""
import factory

from django.utils.timezone import now

from django_libs.tests.factories import UserFactory

from ..models import ObjectEvent, ObjectEventType, ObjectEventSettings
from .test_app.models import DummyModel, TestProfile


class DummyModelFactory(factory.Factory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel

    name = 'Foobar'


class TestProfileFactory(factory.Factory):
    """Factory for the ``TestProfile`` model."""
    FACTORY_FOR = TestProfile

    user = factory.SubFactory(UserFactory)


class ObjectEventTypeFactory(factory.Factory):
    FACTORY_FOR = ObjectEventType

    title = factory.Sequence(lambda x: 'event_type{0}'.format(x))


class ObjectEventFactory(factory.Factory):
    FACTORY_FOR = ObjectEvent

    user = factory.SubFactory(UserFactory)
    creation_date = factory.LazyAttribute(lambda x: now())
    type = factory.SubFactory(ObjectEventTypeFactory)
    content_object = factory.SubFactory(DummyModelFactory)


class ObjectEventSettingsFactory(factory.Factory):
    FACTORY_FOR = ObjectEventSettings
