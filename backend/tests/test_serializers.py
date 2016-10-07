from django.test import TestCase
from rest_framework.exceptions import ValidationError

from backend.models import *
from backend.serializers import *
from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session


class SerializerTestCase(TestCase):
    pass


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
                'email': 'notemail',
                'password': 'password123',
            })

        with self.assertRaises(ValidationError, msg='Password may not be blank'):
            create_user({
                'email': 'exmaple@example.com',
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
            self._patch_user(u, {'email': 'invalid-email'})


class AgendaSerializerTest(SerializerTestCase):
    def setUp(self):
        self.user = create_user(factory.user())

    def _patch_agenda(self, agenda, data):
        s = AgendaSerializer(instance=agenda, data=data, partial=True)
        s.is_valid(True)
        return s.save()

    def test_create_agenda(self):
        create_agenda(self.user, factory.agenda())
        create_agenda(self.user, factory.agenda(full=True))
        self.assertEqual(2, self.user.profile.agenda_set.count())

    def test_update_agenda(self):
        agenda = create_agenda(self.user, factory.agenda())

        agenda = self._patch_agenda(agenda, {
            'name': 'Changed Event Name',
        })
        self.assertEqual(agenda.name, 'Changed Event Name')

        agenda = self._patch_agenda(agenda, {
            'location': 'Shelton Hotel',
            'date': factory.today.isoformat(),
        })
        self.assertEqual(agenda.date, factory.today)
        self.assertEqual(agenda.location, 'Shelton Hotel')

        self._patch_agenda(agenda, data={
            'location': '',
        })
        self.assertEqual(agenda.location, '')


class SessionSerializerTest(SerializerTestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())

    def test_create_session(self):
        create_session(self.agenda, factory.session())
        create_session(self.agenda, factory.session(full=True))

    def test_invalid_session(self):
        negative_duration = factory.session({
            'duration': -30,
        })

        with self.assertRaises(ValidationError):
            create_session(self.agenda, negative_duration)
