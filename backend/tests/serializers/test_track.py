from unittest import TestCase

from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_track


class TrackSerializerTest(TestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())

    def test_created_with_agenda(self):
        self.assertEqual(1, self.agenda.track_set.count())
        self.assertEqual("Track 1", self.agenda.track_set.first().name)

    def test_create(self):
        track = create_track(self.agenda)
        self.assertEqual("Track 2", track.name)

        track = create_track(self.agenda, {'name': 'My custom name'})
        self.assertEqual("My custom name", track.name)
