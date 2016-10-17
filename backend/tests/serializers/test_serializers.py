from datetime import timedelta

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from backend.serializers import *
from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_track


class SerializerTestCase(TestCase):
    pass


class TrackSerializerTest(SerializerTestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())

    def test_create_empty(self):
        t = create_track(self.agenda, {})

    def test_create_filled(self):
        t = create_track(self.agenda, factory.track())


class AgendaSerializerTest(SerializerTestCase):
    def setUp(self):
        self.user = create_user(factory.user())

    def patch_agenda(self, agenda, data):
        s = AgendaSerializer(instance=agenda, data=data, partial=True)
        s.is_valid(True)
        return s.save()

    def test_create_agenda(self):
        agenda = create_agenda(self.user, factory.agenda())
        self.assertEqual(1, agenda.track_set.count())
        create_agenda(self.user, factory.agenda(full=True))
        self.assertEqual(2, self.user.profile.agenda_set.count())

    def test_update_agenda(self):
        agenda = create_agenda(self.user, factory.agenda())

        agenda = self.patch_agenda(agenda, {
            'name': 'Changed Event Name',
        })
        self.assertEqual(agenda.name, 'Changed Event Name')

        agenda = self.patch_agenda(agenda, {
            'location': 'Shelton Hotel',
            'start_at': factory.next_month.date().isoformat(),
        })
        self.assertEqual(agenda.start_at, factory.next_month.date())
        self.assertEqual(agenda.location, 'Shelton Hotel')

        self.patch_agenda(agenda, data={
            'location': '',
        })
        self.assertEqual(agenda.location, '')

    def test_invalid_agenda(self):
        with self.assertRaises(ValidationError):
            create_agenda(self.user, factory.agenda(data={
                'duration': -1,
            }))

        with self.assertRaises(ValidationError):
            create_agenda(self.user, factory.agenda(data={
                'start_at': factory.today - timedelta(days=1),
            }))
