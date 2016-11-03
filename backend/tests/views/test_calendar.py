from icalendar import Calendar
from rest_framework import status
from rest_framework.reverse import reverse

from backend.models import Registration
from backend.tests import factory
from backend.tests.helper import *
from .base import BaseAPITestCase


class CalendarTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda(full=True))
        self.viewer = create_viewer(self.agenda, factory.viewer())
        self.url = self.viewer.get_absolute_url()
        self.sessions = [create_session(self.agenda, factory.session(full=True)) for i in range(10)]
        self.agenda_url = reverse('agenda-calendar', [self.agenda.pk])
        self.viewer_url = reverse('viewer-calendar', [self.agenda.pk, self.viewer.pk])

    def assertIsCalendar(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('attachment', response['content-disposition'])
        self.assertIn('text/calendar', response['content-type'])
        cal = self.to_ics(response)
        self.assertFalse(cal.is_broken)
        return cal

    def to_ics(self, response):
        cal = Calendar()
        cal.from_ical(response.rendered_content.decode("utf-8"), True)
        return cal

    def session_url(self, session_id):
        return reverse('session-calendar', [self.agenda.pk, session_id])

    def test_session(self):
        response = self.client.get(self.session_url(self.sessions[0].pk))
        cal = self.assertIsCalendar(response)
        self.assertTrue(cal.subcomponents)

    def test_agenda(self):
        response = self.client.get(self.agenda_url)
        cal = self.assertIsCalendar(response)

    def test_agenda_incomplete_sessions(self):
        create_session(self.agenda, factory.session())
        response = self.client.get(self.agenda_url)
        cal = self.assertIsCalendar(response)

    def test_viewer_empty(self):
        response = self.client.get(self.viewer_url)
        cal = self.assertIsCalendar(response)

    def test_list_full(self):
        indices = [3, 6, 9, 4]

        for i, n in enumerate(indices):
            session = self.sessions[n]
            Registration.objects.create(session=session, viewer=self.viewer)

        response = self.client.get(self.viewer_url)
        self.assertIsCalendar(response)
