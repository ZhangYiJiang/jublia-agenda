from django.core import mail
from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_viewer
from .base import BaseAPITestCase


class ViewerCreateTest(BaseAPITestCase):
    def setUp(self):
        self.email_count = len(mail.outbox)
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda(full=True))
        self.url = reverse('viewer_create', [self.agenda.pk])

    def testCreate(self):
        response = self.client.post(self.url, factory.viewer())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)


class ViewerRegisterTest(BaseAPITestCase):
    def setUp(self):
        self.email_count = len(mail.outbox)
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda(full=True))
        self.sessions = [create_session(self.agenda, factory.session(full=True)) for i in range(10)]
        self.viewer = create_viewer(self.agenda, factory.viewer())

    def url(self, session_id):
        return reverse('viewer_registration', [self.agenda.pk, self.viewer.token, session_id])

    def testRegister(self):
        response = self.client.put(self.url(self.sessions[0].pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
