from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from .base import BaseAPITestCase


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