from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO

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

        # Calculate the number of minutes from midnight
        mins = int((timezone.now() - timezone.now().replace(hour=0, minute=0, second=0)).total_seconds() / 60)
        self.sessions = create_session(self.agenda, factory.session({
            'start_at': mins + 4,
            'duration': 60,
        }))

        self.viewer = create_viewer(self.agenda, factory.viewer(full=True))
        Registration.objects.create(viewer=self.viewer, session=self.sessions)

    def test_command(self):
        out = StringIO()
        call_command('sendsms', stdout=out)
        self.sessions.refresh_from_db()
        self.assertTrue(self.sessions.is_sms_sent)
