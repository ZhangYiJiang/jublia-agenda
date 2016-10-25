from rest_framework.exceptions import ValidationError

from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_category
from backend.tests.serializers.test_serializers import SerializerTestCase


class CategorySerializerTest(SerializerTestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())

    def test_unique_name(self):
        category = create_category(self.agenda, factory.category())
        with self.assertRaises(ValidationError) as e:
            create_category(self.agenda, factory.category({'name': category.name}))
        self.assertValidationError(e.exception)

    def test_created_with_agenda(self):
        self.assertTrue(self.agenda.category_set.count())
