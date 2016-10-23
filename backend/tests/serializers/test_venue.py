from rest_framework.exceptions import ValidationError

from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_venue
from backend.tests.serializers.test_serializers import SerializerTestCase


class VenueSerializerTest(SerializerTestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())

    def test_unique_name(self):
        venue = create_venue(self.agenda, factory.venue())
        with self.assertRaises(ValidationError) as e:
            create_venue(self.agenda, factory.venue(full=True, data={'name': venue.name}))
        self.assertValidationError(e.exception)
