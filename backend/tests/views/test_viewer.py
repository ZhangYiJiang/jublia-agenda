from django.core import mail
from rest_framework import status
from rest_framework.reverse import reverse

from backend.models import Viewer
from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_viewer
from .base import BaseAPITestCase


class ViewerCreateTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda(full=True))
        self.url = reverse('viewer_create', [self.agenda.pk])
        self.email_count = len(mail.outbox)

    def testCreate(self):
        viewer_data = factory.viewer()
        response = self.client.post(self.url, viewer_data)
        viewer = Viewer.objects.get(email=viewer_data['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(viewer.token, response.data['token'])
        self.assertEmailSent()
        email = mail.outbox[-1]
        self.assertIn(viewer.token, email.body)

    def testDoubleCreate(self):
        viewer_data = factory.viewer()
        first_response = self.client.post(self.url, viewer_data)
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        second_response = self.client.post(self.url, viewer_data)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEmailSent(2)


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
