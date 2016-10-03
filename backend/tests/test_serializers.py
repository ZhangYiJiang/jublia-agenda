from django.test import TestCase
from rest_framework.exceptions import ValidationError

from backend.serializers import *
from backend.models import *
from backend.tests import data


class SerializerTestCase(TestCase):
    def _create_default_user(self):
        return self._create_user(data.user)

    def _create_user(self, data):
        s = UserSerializer(data=data)
        s.is_valid(raise_exception=True)
        return s.save()

    def _create_agenda(self, data):
        user = self._create_default_user()
        s = AgendaSerializer(data=data, context={'user': user})
        s.is_valid(True)
        return s.save()


class UserSerializerTest(SerializerTestCase):
    def _patch_user(self, user, data):
        s = UserSerializer(user, data, partial=True)
        s.is_valid(raise_exception=True)
        return s.save()

    def test_create_user(self):
        user = self._create_user(data.user)
        self.assertIsInstance(user.profile, Profile, 'Profile object not created with user')

    def test_create_user_with_profile(self):
        self._create_user({
            **data.user,
            'company': 'Hello World Corp.'
        })

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
        u = self._create_user(data.user)
        u = self._patch_user(u, {'company': 'Test Company'})
        self.assertEqual(u.profile.company, 'Test Company')

        u = self._patch_user(u, {'company': 'Changed Company'})
        self.assertEqual(u.profile.company, 'Changed Company')

        u = self._patch_user(u, {'company': ''})
        self.assertEqual(u.profile.company, '')

    def test_invalid_update(self):
        u = self._create_user(data.user)

        with self.assertRaises(ValidationError):
            self._patch_user(u, {'email': 'invalid-email'})


class AgendaSerializerTest(SerializerTestCase):
    def _patch_agenda(self, agenda, data):
        s = AgendaSerializer(instance=agenda, data=data, partial=True)
        s.is_valid(True)
        return s.save()

    def test_create_agenda(self):
        self._create_agenda(data.agenda)

    def test_update_agenda(self):
        agenda = self._create_agenda(data.agenda)

        agenda = self._patch_agenda(agenda, {
            'name': 'Changed Event Name',
        })
        self.assertEqual(agenda.name, 'Changed Event Name')

        agenda = self._patch_agenda(agenda, {
            'location': 'Shelton Hotel',
            'date': data.today.isoformat(),
        })
        self.assertEqual(agenda.date, data.today)
        self.assertEqual(agenda.location, 'Shelton Hotel')

        self._patch_agenda(agenda, data={
            'location': '',
        })
