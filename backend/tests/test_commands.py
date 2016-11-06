from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from backend.models import Registration
from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_viewer


class SendSMSCommandTest(TestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        # Set start_at manually to avoid validation error
        self.agenda.start_at = factory.today
        self.agenda.save()

        self.viewer = create_viewer(self.agenda, factory.viewer(full=True))

        # Calculate the number of minutes from midnight
        self.time = int((timezone.now() - timezone.now().replace(hour=0, minute=0, second=0)).total_seconds() / 60) + 15

    def create_session_at(self, offset, data=None):
        if data is None:
            data = {}
        session = create_session(self.agenda, factory.session({
            **data,
            'start_at': self.time + offset,
            'duration': 60,
        }))
        Registration.objects.create(viewer=self.viewer, session=session)
        return session

    def test_command(self):
        session = self.create_session_at(3)
        call_command('sendsms')

        session.refresh_from_db()
        self.assertTrue(session.is_sms_sent)

    def test_range(self):
        session_before = self.create_session_at(-4)
        session_after = self.create_session_at(20)
        call_command('sendsms')

        session_before.refresh_from_db()
        session_after.refresh_from_db()
        self.assertFalse(session_before.is_sms_sent)
        self.assertFalse(session_after.is_sms_sent)

    def test_already_sent(self):
        session = self.create_session_at(3)
        session.is_sms_sent = True
        session.save()
        call_command('sendsms')
