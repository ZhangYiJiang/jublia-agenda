from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import *
from .base import BaseAPITestCase, DetailAuthTestMixin, ListAuthTestMixin


class SessionListTest(ListAuthTestMixin, BaseAPITestCase):
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

        # Check that relations are represented with IDs
        track = self.agenda.track_set.first()
        self.assertEqual(response.data[0]['track'], track.pk)

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

        session_data = factory.session(full=True, data={
            'speakers': [s.pk for s in speakers],
            'track': track.pk,
        })
        response = self.client.post(self.url, session_data)

        self.assertCreatedOk(response)

        # Check that the speakers match, and that the session has been created
        pk = response.data['id']
        self.assertTrue(track.session_set.filter(pk=pk).exists())
        for speaker in speakers:
            self.assertTrue(speaker.session_set.filter(pk=pk).exists())
        self.assertEqualExceptMeta(session_data, response.data, ignore=('popularity',))

    def test_create_on_track(self):
        self.login(self.user)


class SessionDetailTest(DetailAuthTestMixin, BaseAPITestCase):
    def assertSessionEqual(self, original, response, msg=None):
        self.assertEqualExceptMeta(original, response, ignore=('track', 'popularity',))

    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.session_data = factory.session()
        self.session = create_session(self.agenda, self.session_data)
        self.url = self.session.get_absolute_url()

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.session_data['name'])
        self.assertNoEmptyFields(response.data)

        # Check relations
        self.assertIsInstance(response.data['track'], int)

    def test_speaker(self):
        speaker_data = factory.speaker()
        speaker = create_speaker(self.agenda, speaker_data)
        self.session.speakers.add(speaker)
        response = self.client.get(self.url)
        self.assertEqual(speaker.pk, response.data['speakers'][0])

    def test_venue(self):
        venue_data = factory.venue(full=True)
        venue = create_venue(self.agenda, venue_data)
        self.session.venue = venue
        self.session.save()
        response = self.client.get(self.url)
        self.assertEqual(venue.pk, response.data['venue'])

    def test_category(self):
        category = create_category(self.agenda, factory.category(), ['A', 'B', 'C'])
        tags = category.tag_set.all()
        self.session.tags.add(*tags)
        response = self.client.get(self.url)
        for tag in tags:
            self.assertTrue(tag.pk in response.data['categories'][category.pk])

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

