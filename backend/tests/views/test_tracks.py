from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_track
from .base import BaseAPITestCase, ListAuthTestMixin, DetailAuthTestMixin


class TrackListTest(ListAuthTestMixin, BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.session = create_session(self.agenda, factory.session())
        self.url = reverse('track_list', [self.agenda.pk])

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

        create_track(self.agenda)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))
        self.assertFalse('sessions' in response.data[0])

    def test_create(self):
        self.login(self.user)
        track_data = factory.track()
        response = self.client.post(self.url, track_data)
        self.assertCreatedOk(response)
        self.assertEqualExceptMeta(track_data, response.data)


class TrackDetailTest(DetailAuthTestMixin, BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.track = self.agenda.track_set.first()
        self.session = create_session(self.agenda, data=factory.session(data={
            'tracks': [self.track.pk],
        }))
        self.url = self.track.get_absolute_url()

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('sessions' in response.data)

    def test_patch(self):
        self.login(self.user)
        new_data = factory.track()
        response = self.client.patch(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_data['name'], response.data['name'])

    def test_delete(self):
        new_track = create_track(self.agenda)
        self.login(self.user)
        response = self.client.delete(new_track.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, self.agenda.track_set.count())

    def test_delete_last(self):
        # User shouldn't be able to delete the last track
        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsErrorDetail(response.data)
        self.assertEqual(1, self.agenda.track_set.count())

    def test_delete_no_cascade(self):
        # When deleting a track all sessions on it should be transferred to another track
        create_track(self.agenda)
        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.session.refresh_from_db()  # Will raise exception if the session is deleted

    def test_delete_transfer_session(self):
        track_1 = create_track(self.agenda)
        track_2 = create_track(self.agenda)
        self.session.tracks.add(track_1, track_2)

        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.session.refresh_from_db()
        self.assertEqual(2, self.session.tracks.count())
