from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_speaker
from .test_serializers import SerializerTestCase


class SpeakerSerializerTest(SerializerTestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())

    def test_create_speaker(self):
        create_speaker(self.agenda, factory.speaker())
        create_speaker(self.agenda, factory.speaker(full=True))
