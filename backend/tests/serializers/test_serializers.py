from django.test import TestCase

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

    def _patch_agenda(self, agenda, data):
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

        agenda = self._patch_agenda(agenda, {
            'name': 'Changed Event Name',
        })
        self.assertEqual(agenda.name, 'Changed Event Name')

        agenda = self._patch_agenda(agenda, {
            'location': 'Shelton Hotel',
            'start_at': factory.today.isoformat(),
        })
        self.assertEqual(agenda.start_at, factory.today)
        self.assertEqual(agenda.location, 'Shelton Hotel')

        self._patch_agenda(agenda, data={
            'location': '',
        })
        self.assertEqual(agenda.location, '')
