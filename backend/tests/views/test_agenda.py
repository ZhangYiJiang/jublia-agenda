from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import *
from .base import BaseAPITestCase


class AgendaListTest(BaseAPITestCase):
    url = reverse('agenda_list')

    def setUp(self):
        self.user = create_user(factory.user())

    def test_list(self):
        create_agenda(self.user, factory.agenda())
        create_agenda(self.user, factory.agenda(full=True))

        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

        # Agenda list items should not have session data
        self.assertFalse('sessions' in response.data[0])

    def test_list_empty(self):
        self.login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(response.data))

    def test_create(self):
        self.login(self.user)
        agenda_data = factory.agenda(full=True)
        response = self.client.post(self.url, agenda_data)
        self.assertCreatedOk(response)
        response.data.pop('end_at')
        self.assertEqualExceptMeta(agenda_data, response.data)

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url)


class AgendaDetailTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda_data = factory.agenda()
        self.agenda = create_agenda(self.user, self.agenda_data)

        # Session metadata
        self.speaker = create_speaker(self.agenda, factory.speaker())
        self.venue = create_venue(self.agenda, factory.venue())

        self.session = create_session(self.agenda, factory.session(full=True, data={
            'speakers': [self.speaker.pk],
            'venue': self.venue.pk,
        }))

        self.url = reverse('agenda_detail', [self.agenda.pk])

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.agenda_data['name'])
        self.assertNoEmptyFields(response.data)

        # Check related fields
        self.assertTrue('sessions' in response.data)
        self.assertTrue('tracks' in response.data)
        self.assertTrue('speakers' in response.data)
        self.assertTrue('venues' in response.data)

        # Check no deep nesting
        session = response.data['sessions'][0]
        self.assertEqual(self.speaker.pk, session['speakers'][0])
        self.assertEqual(self.agenda.track_set.first().pk, session['track'])
        self.assertEqual(self.venue.pk, session['venue'])
        self.assertFalse('sessions' in response.data['tracks'][0])
        self.assertFalse('sessions' in response.data['speakers'][0])
        self.assertFalse('sessions' in response.data['venues'][0])

    def test_retrieve_end_at(self):
        self.agenda.start_at = factory.now
        self.agenda.save()
        create_session(self.agenda, factory.session(full=True))
        response = self.client.get(self.url)
        self.assertTrue('end_at' in response.data)

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
        self.assertTrue(response.data['name'], 'New Conference Name')
        self.assertNoEmptyFields(response.data)

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url, 'delete')
        self.assert401WhenUnauthenticated(self.url, 'put')
        self.assert401WhenUnauthenticated(self.url, 'patch')

    def test_unauthorized(self):
        self.assert403WhenUnauthorized(self.url, 'delete')
        self.assert403WhenUnauthorized(self.url, 'patch')
        self.assert403WhenUnauthorized(self.url, 'put')
