from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import *
from .base import BaseAPITestCase, DetailAuthTestMixin, ListAuthTestMixin


class SpeakerListTest(ListAuthTestMixin, BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.session = create_session(self.agenda, factory.session())
        self.url = reverse('speaker_list', [self.agenda.pk])

    def test_list(self):
        create_speaker(self.agenda, factory.speaker())
        create_speaker(self.agenda, factory.speaker(full=True))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

    def test_create(self):
        self.login(self.user)
        speaker_data = factory.speaker(full=True)
        response = self.client.post(self.url, speaker_data)
        self.assertCreatedOk(response)
        self.assertEqualExceptMeta(speaker_data, response.data)

    def test_create_with_icon(self):
        self.login(self.user)
        attachment = create_attachment(self.user)
        response = self.client.post(self.url, factory.speaker({'image': attachment.pk}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(TEST_IMAGE_NAME, response.data['image'])


class SpeakerDetailTest(DetailAuthTestMixin, BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.speaker_data = factory.speaker()
        self.speaker = create_speaker(self.agenda, self.speaker_data)
        self.session = create_session(self.agenda, {
            **factory.session(),
            'speakers': [self.speaker.pk],
        })
        self.url = self.speaker.get_absolute_url()

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        self.login(self.user)
        new_data = factory.speaker()
        response = self.client.patch(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_data['name'], response.data['name'])

    def test_put(self):
        self.login(self.user)
        speaker = create_speaker(self.agenda, factory.speaker(full=True))
        data = factory.speaker()
        response = self.client.put(speaker.get_absolute_url(), data)
        self.assertEqualExceptMeta(data, response.data)

    def test_delete(self):
        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.agenda.speaker_set.count())
