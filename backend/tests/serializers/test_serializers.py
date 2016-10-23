from django.test import TestCase
from rest_framework.exceptions import ValidationError

from backend.tests.helper import ErrorDetailMixin


class SerializerTestCase(ErrorDetailMixin, TestCase):
    def assertValidationError(self, error):
        self.assertIsInstance(error, ValidationError)
        self.assertIsErrorDetail(error.detail)
