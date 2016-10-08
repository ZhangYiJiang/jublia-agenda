from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from backend.helper import get_token
from backend.tests import factory
from backend.tests.helper import create_user


class BaseAPITestCase(APITestCase):
    def authenticate(self):
        url = reverse('sign_up')
        response = self.client.post(url, factory.user())
        self.credentials(response.data['token'])

    def login(self, user):
        self.assertTrue(User.objects.filter(email=user.email).exists())
        token = get_token(user)
        self.credentials(token)

    def credentials(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='bearer ' + token)

    def assertNoEmptyFields(self, obj):
        for key, value in obj.items():
            try:
                if len(value) == 0:
                    raise AssertionError("AssertionError: '{}' key is empty".format(key))
            except TypeError:
                pass

    def assertEqualExceptMeta(self, original, response, msg=None):
        self.assertTrue(response.pop('id'))
        response.pop('url', None)
        response.pop('created_at', None)
        response.pop('updated_at', None)
        self.assertEqual(original, response, msg)

    def assert401WhenUnauthenticated(self, url, method='post', data=None):
        response = getattr(self.client, method.lower())(url, data=data)
        message = "Request to {} should have resulted in 401 Unauthorized".format(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, message)

    def assert403WhenUnauthorized(self, url, method='post', data=None):
        another_user = create_user(factory.user())
        self.login(another_user)
        message = "Request to {} should have resulted in 403 Forbidden".format(url)
        response = getattr(self.client, method.lower())(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, message)


class UserViewTest(BaseAPITestCase):
    user_url = reverse('user')
    sign_up_url = reverse('sign_up')

    def test_sign_up(self):
        response = self.client.post(self.sign_up_url, factory.user())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

    def test_sign_up_with_event(self):
        user_with_event = factory.user({
            'event_name': 'JSConf.asia',
        })
        user_response = self.client.post(self.sign_up_url, user_with_event)
        self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)

        # Check that a event was created with the user
        self.credentials(user_response.data['token'])
        agenda_response = self.client.get(reverse('agenda_list'))
        self.assertEqual(agenda_response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(agenda_response.data))

    def test_get_user(self):
        self.authenticate()
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse('password' in response.data)

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.user_url)
