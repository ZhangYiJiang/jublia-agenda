from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import create_session, create_user, create_agenda
from backend.tests.views.test_views import BaseAPITestCase


class SessionListTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.url = reverse('session_list', args=[self.agenda.pk])

    def test_list(self):
        self.agenda.session_set.create(**factory.session())
        self.agenda.session_set.create(**factory.session(full=True))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

    def test_list_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(response.data))

    def test_create(self):
        self._login(self.user)
        response = self.client.post(self.url, factory.session())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.has_header('location'))
        self.assertNoEmptyFields(response.data)

    def test_create_unauthenticated(self):
        response = self.client.post(self.url, factory.session())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SessionDetailTest(BaseAPITestCase):
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

    def test_delete(self):
        self._login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch(self):
        self._login(self.user)
        response = self.client.patch(self.url, {
            'name': 'New Conference Name'
        })
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['name'], 'New Conference Name')
        self.assertNoEmptyFields(response.data)

    def test_delete_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_unauthorized(self):
        user = create_user({
            'email': 'another-user@example.com',
            'password': 'another test password'
        })
        self._login(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)