from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from backend.helper import get_token
from backend.tests import data
from backend.tests.helper import create_user, create_default_user, create_default_agenda, create_session


class BaseAPITestCase(APITestCase):
    def _authenticate(self):
        url = reverse('sign_up')
        response = self.client.post(url, data.user)
        self.client.credentials(HTTP_AUTHORIZATION='bearer ' + response.data['token'])

    def _login(self, user):
        self.assertTrue(User.objects.filter(email=user.email).exists())
        token = get_token(user)
        self.client.credentials(HTTP_AUTHORIZATION='bearer ' + token)


class UserViewTest(BaseAPITestCase):
    url = reverse('user')

    def test_sign_up(self):
        url = reverse('sign_up')
        response = self.client.post(url, data.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

    def test_get_user(self):
        self._authenticate()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse('password' in response.data)

    def test_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AgendaListTest(BaseAPITestCase):
    url = reverse('agenda_list')

    def test_create(self):
        self._authenticate()
        response = self.client.post(self.url, data.agenda)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.has_header('location'))

    def test_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AgendaDetailTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_default_user()
        self.agenda = create_default_agenda()
        self.url = reverse('agenda_detail', [self.agenda.pk])

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data.agenda['name'])

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


class SessionListTest(BaseAPITestCase):
    def setUp(self):
        self.agenda = create_default_agenda()
        self.url = reverse('session_list', args=[self.agenda.pk])
        self.user = create_default_user()

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        self._login(self.user)
        response = self.client.post(self.url, data.session)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.has_header('location'))

    def test_create_unauthenticated(self):
        response = self.client.post(self.url, data.session)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SessionDetailTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_default_user()
        self.agenda = create_default_agenda()
        self.session = create_session(self.agenda, data.session)
        self.url = reverse('session_detail', args=[self.agenda.pk, self.session.pk])

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data.session['name'])

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

