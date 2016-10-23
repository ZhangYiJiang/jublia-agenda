from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import *
from .base import BaseAPITestCase, DetailAuthTestMixin, ListAuthTestMixin


class VenueListTest(ListAuthTestMixin, BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.session = create_session(self.agenda, factory.session())
        self.url = reverse('venue_list', [self.agenda.pk])

    def test_list(self):
        create_venue(self.agenda, factory.venue())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

        create_venue(self.agenda, factory.venue(full=True))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))
        self.assertFalse('sessions' in response.data[0])

    def test_create(self):
        self.login(self.user)
        venue_data = factory.venue(full=True)
        response = self.client.post(self.url, venue_data)
        self.assertCreatedOk(response)
        self.assertEqualExceptMeta(venue_data, response.data)


class VenueDetailTest(DetailAuthTestMixin, BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.venue = create_venue(self.agenda, factory.venue())
        self.session = create_session(self.agenda, data=factory.session(data={'venue': self.venue.pk}))
        self.url = self.venue.get_absolute_url()

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('sessions' in response.data)

    def test_patch(self):
        self.login(self.user)
        new_data = factory.venue()
        response = self.client.patch(self.url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_data['name'], response.data['name'])

    def test_delete(self):
        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, self.agenda.venue_set.count())

    def test_delete_no_cascade(self):
        # Deleting a venue should not cause the session to disappear
        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.session.refresh_from_db()  # Will raise exception if the session is deleted
