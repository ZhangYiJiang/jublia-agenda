from datetime import timedelta

from rest_framework.exceptions import ValidationError

from backend.serializers import AgendaSerializer
from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session
from backend.tests.serializers.test_serializers import SerializerTestCase


class AgendaSerializerTest(SerializerTestCase):
    def setUp(self):
        self.user = create_user(factory.user())

    def patch_agenda(self, agenda, data):
        s = AgendaSerializer(instance=agenda, data=data, partial=True, context={
            'user': self.user,
        })
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

    def test_duplicate_agenda(self):
        agenda_data = factory.agenda(full=True)
        create_agenda(self.user, agenda_data)
        with self.assertRaises(ValidationError):
            create_agenda(self.user, factory.agenda(full=True, data={
                'name': agenda_data['name'],
            }))

    def test_duration_cut_session(self):
        agenda = create_agenda(self.user, factory.agenda())
        create_session(agenda, factory.session(data={
            'start_at': 23 * 60,  # Right between two days
            'duration': 120,
        }))

        with self.assertRaises(ValidationError):
            self.patch_agenda(agenda, {
                'duration': 1,
            })

        # Check that two days is fine
        create_session(agenda, factory.session(data={
            'start_at': 36 * 60,  # 36 hours = 12pm, second day
            'duration': 60,
        }))
        self.patch_agenda(agenda, {
            'duration': 2,
        })
