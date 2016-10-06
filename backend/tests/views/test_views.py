from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from backend.helper import get_token
from backend.tests import data


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


