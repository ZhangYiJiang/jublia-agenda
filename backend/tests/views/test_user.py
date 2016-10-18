from django.contrib.auth.models import User
from django.core import mail
from rest_framework import status
from rest_framework.reverse import reverse

from backend.models import Agenda
from backend.tests import factory
from backend.tests.helper import create_user
from .base import BaseAPITestCase


class UserViewTest(BaseAPITestCase):
    user_url = reverse('user')
    login_url = reverse('auth')
    sign_up_url = reverse('sign_up')

    def setUp(self):
        self.email_count = len(mail.outbox)

    def test_sign_up(self):
        user_data = factory.user()
        response = self.client.post(self.sign_up_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('data' not in response or 'token' not in response.data)
        self.assertEmailSent()

        # Check that the user can't sign in yet
        login_response = self.client.post(self.login_url, user_data)
        self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_event(self):
        user_with_event = factory.user({
            'event_name': 'JSConf.asia',
        })
        user_response = self.client.post(self.sign_up_url, user_with_event)
        self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)
        self.assertEmailSent()

        # Check that a event was created with the user
        self.assertTrue(Agenda.objects.filter(name='JSConf.asia').count())

    def test_verification(self):
        user_data = factory.user()
        self.client.post(self.sign_up_url, user_data)

        # Check that the verification email was send with token
        profile = User.objects.get(username=user_data['username']).profile
        self.assertEmailSent()
        email = mail.outbox[-1]
        self.assertIn(profile.verification_token, email.body)
        self.assertIn('http', email.body, 'URL in verification email need to be full URLs')

        # Request for another verification email
        response = self.client.post(reverse('resend_verification'), {'username': user_data['username']})
        self.assertEmailSent(2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        email = mail.outbox[-1]
        profile.refresh_from_db()
        self.assertIn(profile.verification_token, email.body)

        # Check that the verification
        response = self.client.get(reverse('verify_email', [profile.verification_token]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('token', response['location'])

        # Check that sign in afterwards works
        response = self.client.post(self.login_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        user_data = factory.user()
        user = create_user(user_data)
        self.login(user)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse('password' in response.data)

    def test_update_user(self):
        user_data = factory.user()
        user = create_user(user_data)
        self.login(user)

        new_data = factory.user(full=True)
        response = self.client.put(self.user_url, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k in ('username', 'company'):
            self.assertEqual(new_data[k], response.data[k])

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.user_url)