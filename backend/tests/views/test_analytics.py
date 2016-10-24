import random
from collections import defaultdict
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse

from backend.models import Registration, Viewer
from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_viewer
from .base import BaseAPITestCase


class TestAnalyticsView(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.session = create_session(self.agenda, factory.session())
        self.url = reverse('analytics', [self.agenda.pk])

    def create_registrations(self, session, count=10):
        Viewer.objects.bulk_create([Viewer(agenda=self.agenda, **factory.viewer()) for i in range(count)])

        registrations = []
        for viewer in self.agenda.viewer_set.all():
            registrations.append(Registration(session=session, viewer=viewer))
        Registration.objects.bulk_create(registrations)

    def test_empty(self):
        create_viewer(self.agenda, factory.viewer())
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.session.pk, response.data)

    def test_one_day(self):
        self.create_registrations(self.session)

        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(10, response.data[self.session.pk].values())

    def test_multiple_days(self):
        self.create_registrations(self.session)
        dates = defaultdict(int)
        for pk in Registration.objects.values_list('pk', flat=True):
            # Create random datetimes from today to 7 days ago
            time = timezone.now() - timedelta(minutes=random.randint(0, 24 * 60 * 7))
            dates[time.date().isoformat()] += 1
            Registration.objects.filter(pk=pk).update(created_at=time)

        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(dict(response.data[self.session.pk]), dict(dates))

    def test_multiple_session(self):
        count = 5
        Viewer.objects.bulk_create([Viewer(agenda=self.agenda, **factory.viewer()) for i in range(count)])
        viewers = self.agenda.viewer_set.all()

        sessions = []
        for i in range(5):
            session = create_session(self.agenda, factory.session(full=True))
            sessions.append(session)
            Registration.objects.bulk_create([Registration(session=session, viewer=v) for v in viewers])

        self.login(self.user)
        response = self.client.get(self.url)
        date = timezone.now().date().isoformat()
        for session in sessions:
            self.assertEqual(count, response.data[session.pk][date])

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url, 'get')

    def test_unauthorized(self):
        self.assert403WhenUnauthorized(self.url, 'get')
