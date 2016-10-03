from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from backend.tests import data


class BaseAPITestCase(APITestCase):
    def _authenticate(self):
        url = reverse('sign_up')
        response = self.client.post(url, data.user)
        self.client.credentials(HTTP_AUTHORIZATION='bearer ' + response.data['token'])


class UserViewTest(BaseAPITestCase):
    def setUp(self):
        self.url = reverse('user')

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
    def setUp(self):
        self.url = reverse('agenda_list')

    def test_create(self):
        self._authenticate()
        response = self.client.post(self.url, data.agenda)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
