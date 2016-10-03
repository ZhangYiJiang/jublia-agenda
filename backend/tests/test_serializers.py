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
        s = UserSerializer(user, data, partial=True)
        s.is_valid(raise_exception=True)
        return s.save()

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

    def test_update_user(self):
        u = self._create_user(self.data)
        u = self._patch_user(u, {'company': 'Test Company'})
        self.assertEqual(u.profile.company, 'Test Company')

        u = self._patch_user(u, {'company': 'Changed Company'})
        self.assertEqual(u.profile.company, 'Changed Company')

        u = self._patch_user(u, {'company': ''})
        self.assertEqual(u.profile.company, '')
