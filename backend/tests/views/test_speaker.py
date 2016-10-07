from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_speaker
from .test_views import BaseAPITestCase


class SpeakerListTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.session = create_session(self.agenda, factory.agenda())
        self.url = reverse('speaker_list', [self.agenda.pk])

    def test_list(self):
        create_speaker(self.agenda, factory.speaker())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

    def test_create(self):
        self._login(self.user)
        response = self.client.post(self.url, factory.speaker())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized(self):
        another_user = create_user(factory.user())
        self._login(another_user)
        response = self.client.post(self.url, factory.speaker())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
