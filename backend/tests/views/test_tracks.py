from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_track
from .base import BaseAPITestCase


class TrackListTest(BaseAPITestCase):
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
        response = self.client.post(self.url, factory.track())
        self.assertCreatedOk(response)

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url)

    def test_unauthorized(self):
        self.assert403WhenUnauthorized(self.url)


class TrackDetailTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.track = self.agenda.track_set.first()
        self.session = create_session(self.agenda, data=factory.session(data={'track': self.track.pk}))
        self.url = reverse('track_detail', [self.agenda.pk, self.track.pk])

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
        self.assertEqual(1, self.agenda.track_set.count())

    def test_delete_no_cascade(self):
        # When deleting a track all sessions on it should be transferred to another track
        create_track(self.agenda)
        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.session.refresh_from_db()  # Will raise exception if the session is deleted

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url, method='patch')
        self.assert401WhenUnauthenticated(self.url, method='put')
        self.assert401WhenUnauthenticated(self.url, method='delete')

    def test_unauthorized(self):
        self.assert403WhenUnauthorized(self.url, method='patch')
        self.assert403WhenUnauthorized(self.url, method='put')
        self.assert403WhenUnauthorized(self.url, method='delete')
