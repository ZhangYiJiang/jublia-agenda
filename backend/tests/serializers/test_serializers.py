from django.test import TestCase
from rest_framework.exceptions import ValidationError

from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_track, ErrorDetailMixin


class SerializerTestCase(ErrorDetailMixin, TestCase):
    def assertValidationError(self, error):
        self.assertIsInstance(error, ValidationError)
        self.assertIsErrorDetail(error.detail)


class TrackSerializerTest(SerializerTestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())

    def test_create_empty(self):
        t = create_track(self.agenda, {})

    def test_create_filled(self):
        t = create_track(self.agenda, factory.track())
