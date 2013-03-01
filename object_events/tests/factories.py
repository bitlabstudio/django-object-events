"""Factories of the ``object_events`` app."""
import factory

from django.utils.timezone import now

from django_libs.tests.factories import UserFactory

from ..models import ObjectEvent, ObjectEventType
from .test_app.models import DummyModel


class DummyModelFactory(factory.Factory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel

    name = 'Foobar'


class ObjectEventTypeFactory(factory.Factory):
    FACTORY_FOR = ObjectEventType

    title = 'event_type'


class ObjectEventFactory(factory.Factory):
    FACTORY_FOR = ObjectEvent

    user = factory.SubFactory(UserFactory)
    creation_date = factory.LazyAttribute(lambda x: now())
    type = factory.SubFactory(ObjectEventTypeFactory)
    content_object = factory.SubFactory(DummyModelFactory)
