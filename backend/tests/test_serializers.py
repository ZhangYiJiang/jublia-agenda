from django.test import TestCase
from rest_framework.exceptions import ValidationError

from backend.serializers import *
from backend.models import *


class UserSerializerTest(TestCase):
    data = {
        'email': 'hello@example.com',
        'password': 'password12345',
    }

    data_with_profile = {
        'email': 'hello@example.com',
        'password': 'password12345',
        'company': 'Hello World Corp.'
    }

    def _create_user(self, data):
        s = UserSerializer(data=data)
        s.is_valid(raise_exception=True)
        user = s.save()
        self.assertIsInstance(user.profile, Profile, 'Profile object not created with user')
        return user

    def _patch_user(self, user, data):
        s = UserSerializer(user, data)

    def test_create_user(self):
        self._create_user(self.data)

    def test_create_user_with_profile(self):
        self._create_user(self.data_with_profile)

    def test_invalid_user(self):
        with self.assertRaises(ValidationError, msg='Invalid email not rejected'):
            self._create_user({
                'email': 'notemail',
                'password': 'password123',
            })

        with self.assertRaises(ValidationError, msg='Password may not be blank'):
            self._create_user({
                'email': 'exmaple@example.com',
                'password': '',
            })
