from django.test import TestCase

from backend.serializers import *
from backend.tests import factory
from backend.tests.helper import create_user, create_agenda


class SerializerTestCase(TestCase):
    pass


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
