from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_speaker
from .base import BaseAPITestCase


class SpeakerListTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.session = create_session(self.agenda, factory.session())
        self.url = reverse('speaker_list', [self.agenda.pk])

    def test_list(self):
        first_speaker = factory.speaker()
        create_speaker(self.agenda, first_speaker)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))
        self.assertEqualExceptMeta(first_speaker, response.data[0])

    def test_create(self):
        self.login(self.user)
        response = self.client.post(self.url, factory.speaker())
        self.assertCreatedOk(response)

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url)

    def test_unauthorized(self):
        self.assert403WhenUnauthorized(self.url)


class SpeakerDetailTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.speaker_data = factory.speaker()
        self.speaker = create_speaker(self.agenda, self.speaker_data)
        self.session = create_session(self.agenda, {
            **factory.session(),
            'speakers': [self.speaker.pk],
        })
        self.url = reverse('speaker_detail', [self.agenda.pk, self.speaker.pk])

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        self.login(self.user)
        new_data = factory.speaker()
        response = self.client.patch(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_data['name'], response.data['name'])

    def test_delete(self):
        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.agenda.speaker_set.count())

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url, method='patch')
        self.assert401WhenUnauthenticated(self.url, method='put')
        self.assert401WhenUnauthenticated(self.url, method='delete')

    def test_unauthorized(self):
        self.assert403WhenUnauthorized(self.url, method='patch')
        self.assert403WhenUnauthorized(self.url, method='put')
        self.assert403WhenUnauthorized(self.url, method='delete')
