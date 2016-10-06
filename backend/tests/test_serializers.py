from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from backend.serializers import *
from backend.models import *
from backend.tests import data


def create_user(data):
    s = UserSerializer(data=data)
    s.is_valid(raise_exception=True)
    return s.save()


def create_default_user():
    user = User.objects.filter(email=data.user['email']).first()
    if user:
        return user
    return create_user(data.user)


def create_agenda(data):
    user = create_default_user()
    s = AgendaSerializer(data=data, context={'user': user})
    s.is_valid(True)
    return s.save()


def create_default_agenda():
    return create_agenda(data.agenda)


class SerializerTestCase(TestCase):
    pass


class UserSerializerTest(SerializerTestCase):
    def _patch_user(self, user, data):
        s = UserSerializer(user, data, partial=True)
        s.is_valid(raise_exception=True)
        return s.save()

    def test_create_user(self):
        user = create_user(data.user)
        self.assertIsInstance(user.profile, Profile, 'Profile object not created with user')

    def test_create_user_with_profile(self):
        create_user({
            **data.user,
            'company': 'Hello World Corp.'
        })

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
        u = create_user(data.user)
        u = self._patch_user(u, {'company': 'Test Company'})
        self.assertEqual(u.profile.company, 'Test Company')

        u = self._patch_user(u, {'company': 'Changed Company'})
        self.assertEqual(u.profile.company, 'Changed Company')

        u = self._patch_user(u, {'company': ''})
        self.assertEqual(u.profile.company, '')

    def test_invalid_update(self):
        u = create_user(data.user)

        with self.assertRaises(ValidationError):
            self._patch_user(u, {'email': 'invalid-email'})


class AgendaSerializerTest(SerializerTestCase):
    def _patch_agenda(self, agenda, data):
        s = AgendaSerializer(instance=agenda, data=data, partial=True)
        s.is_valid(True)
        return s.save()

    def test_create_agenda(self):
        create_agenda(data.agenda)
        create_agenda(data.full_agenda)

    def test_update_agenda(self):
        agenda = create_agenda(data.agenda)

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
        self.assertEqual(agenda.location, '')


class SessionSerializerTest(SerializerTestCase):
    def _create_session(self, data):
        agenda = create_default_agenda()
        s = SessionSerializer(data=data, context={'agenda': agenda})
        s.is_valid(True)
        return s.save()

    def test_create_session(self):
        self._create_session(data.session)
        self._create_session(data.full_session)
