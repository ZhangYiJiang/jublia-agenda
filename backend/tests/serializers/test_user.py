from rest_framework.exceptions import ValidationError

from backend.models import Profile
from backend.serializers import UserSerializer
from backend.tests import factory
from backend.tests.helper import create_user
from backend.tests.serializers.test_serializers import SerializerTestCase


class UserSerializerTest(SerializerTestCase):
    def _patch_user(self, user, data):
        s = UserSerializer(user, data, partial=True)
        s.is_valid(raise_exception=True)
        return s.save()

    def test_create_user(self):
        user = create_user(factory.user())
        self.assertIsInstance(user.profile, Profile, 'Profile object not created with user')

    def test_create_user_with_profile(self):
        create_user(factory.user(full=True))

    def test_invalid_user(self):
        with self.assertRaises(ValidationError, msg='Invalid email not rejected'):
            create_user({
                'username': 'notemail',
                'password': 'password123',
            })

        with self.assertRaises(ValidationError, msg='Password may not be blank'):
            create_user({
                'username': 'exmaple@example.com',
                'password': '',
            })

    def test_update_user(self):
        u = create_user(factory.user())
        u = self._patch_user(u, {'company': 'Test Company'})
        self.assertEqual(u.profile.company, 'Test Company')

        u = self._patch_user(u, {'company': 'Changed Company'})
        self.assertEqual(u.profile.company, 'Changed Company')

        u = self._patch_user(u, {'company': ''})
        self.assertEqual(u.profile.company, '')

    def test_invalid_update(self):
        u = create_user(factory.user())

        with self.assertRaises(ValidationError):
            self._patch_user(u, {'username': 'invalid-email'})