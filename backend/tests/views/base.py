import os
from functools import wraps

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from backend.helper import get_token
from backend.tests import factory
from backend.tests.helper import create_user, ErrorDetailMixin


def clear_media(func):
    @wraps(func)
    def clear_media_decorator(*args, **kwargs):
        func(*args, **kwargs)
        for f in os.scandir(settings.MEDIA_ROOT):
            if f.name != '.gitignore':
                os.remove(f.path)
    return clear_media_decorator


class BaseAPITestCase(ErrorDetailMixin, APITestCase):
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

    def assertEqualExceptMeta(self, original, response, msg=None, ignore=()):
        """Checks that the dict representing the response is the same as the original data
        except some common model properties
        """
        self.assertTrue(response.pop('id'))  # Sanity check that ID > 0
        response.pop('url', None)
        response.pop('created_at', None)
        response.pop('updated_at', None)
        response.pop('slug', None)
        for field in ignore:
            response.pop(field, None)
        self.assertEqual(original, dict(response), msg)

    def assertIsRedirect(self, response, path=None):
        """A less strict version of assertRedirects
        This method only check response code is in 3XX range and optionally if path matches"""
        self.assertIn(response.status_code, range(300, 400), str(response) + ' is not a redirect')
        if path:
            self.assertEqual(response['location'], path)

    def assert401WhenUnauthenticated(self, url, method='post', data=None):
        response = getattr(self.client, method.lower())(url, data=data)
        message = "Request to {} should have resulted in 401 Unauthorized".format(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, message)

    def assert403WhenUnauthorized(self, url, method='post', data=None):
        another_user = create_user(factory.user())
        self.login(another_user)
        message = "Request to {} from another user should have resulted in 403 Forbidden".format(url)
        response = getattr(self.client, method.lower())(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, message)

    def assertEmailSent(self, count=1):
        if not hasattr(self, 'email_count'):
            raise AssertionError("Please add 'self.email_count = len(mail.outbox)' to the "
                                 "test setUp method (remember to place it AFTER any create_user)")
        self.assertEqual(count, len(mail.outbox) - self.email_count,
                         "Expected %d emails to have been sent" % count)


class ListAuthTestMixin:
    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url)

    def test_unauthorized(self):
        self.assert403WhenUnauthorized(self.url)


class DetailAuthTestMixin:
    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url, method='patch')
        self.assert401WhenUnauthenticated(self.url, method='put')
        self.assert401WhenUnauthenticated(self.url, method='delete')

    def test_unauthorized(self):
        self.assert403WhenUnauthorized(self.url, method='patch')
        self.assert403WhenUnauthorized(self.url, method='put')
        self.assert403WhenUnauthorized(self.url, method='delete')
