from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from backend.tests.data import user_data

factory = APIRequestFactory()


class UserViewTest(APITestCase):
    def _sign_up(self, data):
        url = reverse('sign_up')
        return self.client.post(url, data)

    def test_sign_up(self):
        response = self._sign_up(user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

    def test_get_user(self):
        sign_up = self._sign_up(user_data)
        self.client.credentials(HTTP_AUTHORIZATION='bearer ' + sign_up.data['token'])
        url = reverse('user')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse('password' in response.data)

    def test_unauthenticated(self):
        url = reverse('user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
