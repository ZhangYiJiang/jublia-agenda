from rest_framework.exceptions import ValidationError

from backend.serializers import SessionUpdateSerializer
from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_speaker
from backend.tests.serializers.test_serializers import SerializerTestCase


class SessionSerializerTest(SerializerTestCase):
    # Invalid test cases
    negative_duration = {
        'duration': -30,
    }

    start_without_duration = {
        'start_at': factory.now.isoformat()
    }

    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())

    def update_session(self, session, data):
        s = SessionUpdateSerializer(data=data, instance=session, partial=True)
        s.is_valid(True)
        return s.save()

    def replace_session(self, session, data):
        s = SessionUpdateSerializer(data=data, instance=session)
        s.is_valid(True)
        return s.save()

    def test_create_session(self):
        # Creating basic session
        data = factory.session()
        s = create_session(self.agenda, data)
        self.assertEqual(s.name, data['name'])

        # Creating full sessions
        data = factory.session(full=True)
        s = create_session(self.agenda, data)
        self.assertEqual(s.name, data['name'])
        self.assertEqual(s.start_at, data['start_at'])
        self.assertEqual(s.duration, data['duration'])
        self.assertEqual(s.description, data['description'])

    def test_update_session(self):
        s = create_session(self.agenda, factory.session())

        self.update_session(s, {
            'duration': 45,
            'start_at': 600,
        })
        self.assertEqual(45, s.duration)
        self.assertEqual(600, s.start_at)

        self.update_session(s, {
            'name': 'The most amazing session ever',
        })
        self.assertEqual('The most amazing session ever', s.name)

    def test_put_session(self):
        s = create_session(self.agenda, factory.session(full=True))
        data = factory.session()
        self.replace_session(s, data)
        self.assertEqual(s.name, data['name'])
        self.assertIsNone(s.start_at)
        self.assertIsNone(s.duration)
        self.assertEqual(s.description, '')

    def test_speaker_field(self):
        speaker = create_speaker(self.agenda, factory.speaker())
        session = create_session(self.agenda, {
            **factory.session(full=True),
            'speakers': [speaker.pk],
        })

    def test_invalid_session(self):
        with self.assertRaises(ValidationError):
            create_session(self.agenda, self.negative_duration)

        with self.assertRaises(ValidationError):
            create_session(self.agenda, self.start_without_duration)

    def test_invalid_update(self):
        s = create_session(self.agenda, factory.session())

        with self.assertRaises(ValidationError):
            self.update_session(s, self.negative_duration)

        with self.assertRaises(ValidationError):
            self.update_session(s, self.start_without_duration)
