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

    def assertCreatedOk(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNoEmptyFields(response.data)
        self.assertTrue(response.has_header('location'))

        # Check that the object has actually been created at the location
        pk = response.data['id']
        get_response = self.client.get(response['location'])
        self.assertTrue(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['id'], pk)

    def assertEqualExceptMeta(self, original, response, msg=None):
        self.assertTrue(response.pop('id'))
        response.pop('url', None)
        response.pop('created_at', None)
        response.pop('updated_at', None)
        self.assertEqual(original, dict(response), msg)

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


