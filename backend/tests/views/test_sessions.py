from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import *
from .base import BaseAPITestCase


class SessionListTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.url = reverse('session_list', args=[self.agenda.pk])

    def test_list(self):
        create_session(self.agenda, factory.session())
        create_session(self.agenda, factory.session(full=True))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

    def test_list_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(response.data))

    def test_create(self):
        self.login(self.user)
        response = self.client.post(self.url, factory.session())
        self.assertCreatedOk(response)

    def test_create_full(self):
        self.login(self.user)
        track = create_track(self.agenda)
        speakers = [
            create_speaker(self.agenda, factory.speaker()),
            create_speaker(self.agenda, factory.speaker(full=True)),
        ]

        response = self.client.post(self.url, factory.speaker(full=True, data={
            'speakers': [s.pk for s in speakers],
            'track': track.pk,
        }))

        self.assertCreatedOk(response)

        pk = response.data['id']
        self.assertTrue(track.session_set.filter(pk=pk).exists())
        for speaker in speakers:
            self.assertTrue(speaker.session_set.filter(pk=pk).exists())

    def test_create_on_track(self):
        self.login(self.user)

    def test_create_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url)

    def test_create_unauthorized(self):
        self.assert403WhenUnauthorized(self.url)


class SessionDetailTest(BaseAPITestCase):
    def assertSessionEqual(self, original, response, msg=None):
        response.pop('track')
        self.assertEqualExceptMeta(original, response)

    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.session_data = factory.session()
        self.session = create_session(self.agenda, self.session_data)
        self.url = reverse('session_detail', args=[self.agenda.pk, self.session.pk])

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.session_data['name'])
        self.assertNoEmptyFields(response.data)

        # Check relations
        self.assertTrue('name' in response.data['track'])

    def test_speaker(self):
        speaker_data = factory.speaker()
        speaker = create_speaker(self.agenda, speaker_data)
        self.session.speakers.add(speaker)
        response = self.client.get(self.url)
        self.assertEqualExceptMeta(speaker_data, response.data['speakers'][0])

    def test_venue(self):
        venue_data = factory.venue(full=True)
        venue = create_venue(self.agenda, venue_data)
        self.session.venue = venue
        self.session.save()
        response = self.client.get(self.url)
        self.assertEqualExceptMeta(venue_data, response.data['venue'])

    def test_delete(self):
        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch(self):
        self.login(self.user)

        response = self.client.patch(self.url, {
            'name': 'New Conference Name'
        })
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Conference Name')
        self.assertNoEmptyFields(response.data)

        # Test attaching speakers
        speakers = [
            create_speaker(self.agenda, factory.speaker()).pk,
            create_speaker(self.agenda, factory.speaker()).pk,
            create_speaker(self.agenda, factory.speaker()).pk,
        ]
        response = self.client.patch(self.url, {
            'speakers': speakers,
        })
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, len(response.data['speakers']))
        self.assertNoEmptyFields(response.data)

    def test_put(self):
        self.login(self.user)
        data = factory.session(full=True)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSessionEqual(data, response.data)

        data = factory.session()
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSessionEqual(data, response.data)

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url, 'delete')
        self.assert401WhenUnauthenticated(self.url, 'put')
        self.assert401WhenUnauthenticated(self.url, 'patch')

    def test_unauthorized(self):
        self.assert403WhenUnauthorized(self.url, 'delete')
        self.assert403WhenUnauthorized(self.url, 'patch')
        self.assert403WhenUnauthorized(self.url, 'put')
