from django.core import mail
from rest_framework import status
from rest_framework.reverse import reverse

from backend.models import Registration
from backend.models import Viewer
from backend.tests import factory
from backend.tests.helper import create_user, create_agenda, create_session, create_viewer
from .base import BaseAPITestCase


class ViewerCreateTest(BaseAPITestCase):
    view_name = 'viewer_create'

    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda(full=True))
        self.url = reverse(self.view_name, [self.agenda.pk])
        self.email_count = len(mail.outbox)

    def test_create(self):
        viewer_data = factory.viewer()
        response = self.client.post(self.url, viewer_data)
        viewer = Viewer.objects.get(email=viewer_data['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(viewer.token, response.data['token'])
        self.assertEmailSent()
        email = mail.outbox[-1]
        self.assertIn(viewer.link(), email.body)

    def test_create_full(self):
        viewer_data = factory.viewer(full=True)
        response = self.client.post(self.url, viewer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        viewer = Viewer.objects.get(email=viewer_data['email'])
        self.assertEqual(viewer_data['mobile'], viewer.mobile)

    def test_double_create(self):
        viewer_data = factory.viewer()
        first_response = self.client.post(self.url, viewer_data)
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

        second_response = self.client.post(self.url, viewer_data)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsErrorDetail(second_response.data)
        self.assertEmailSent(2)

    def test_multiple_agenda(self):
        viewer = factory.viewer()
        tokens = set()

        for i in range(5):
            agenda = create_agenda(self.user, factory.agenda())
            url = reverse(self.view_name, [agenda.pk])
            # Create the same viewer on multiple agendas and check that each
            # token is unique
            response = self.client.post(url, viewer)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertNotIn(response.data['token'], tokens)
            tokens.add(response.data['token'])
        self.assertEmailSent(5)


class ViewerRegisterTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda(full=True))
        self.viewer = create_viewer(self.agenda, factory.viewer())

    def url(self, session_id, token=None):
        if token is None:
            token = self.viewer.token
        return reverse('viewer_registration', [self.agenda.pk, token, session_id])

    def test_register(self):
        session = create_session(self.agenda, factory.session(full=True))
        response = self.client.put(self.url(session.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(session.name, self.viewer.sessions.first().name)

        # Check that registering twice doesn't change anything
        response = self.client.put(self.url(session.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, self.viewer.sessions.count())

    def test_unregister(self):
        sessions = [create_session(self.agenda, factory.session(full=True)) for i in range(10)]
        for i, session in enumerate(sessions):
            response = self.client.put(self.url(session.pk))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(i+1, self.viewer.sessions.count())

        response = self.client.delete(self.url(sessions[3].pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(9, self.viewer.sessions.count())
        self.assertNotIn(sessions[3], self.viewer.sessions.all())

    def test_popularity(self):
        session = create_session(self.agenda, factory.session())
        viewers = [create_viewer(self.agenda, factory.viewer()) for i in range(10)]
        # Viewers in the set = 2, 5, 6, 9
        for i in [2, 5, 6, 9]:
            self.client.put(self.url(session.pk, viewers[i].token))
        session.refresh_from_db()
        self.assertEqual(4, session.popularity)

        # Calls put 5 times, but with one repeat
        # Viewers in the set = 0, 1, 2, 3, 4, 5, 6, 9
        for i in [0, 1, 2, 3, 4]:
            self.client.put(self.url(session.pk, viewers[i].token))
        session.refresh_from_db()
        self.assertEqual(8, session.popularity)

        # Viewers in the set = 1, 2, 4, 5, 9
        for i in [0, 3, 6, 7]:
            self.client.delete(self.url(session.pk, viewers[i].token))
        session.refresh_from_db()
        self.assertEqual(5, session.popularity)

    def test_register_error(self):
        response = self.client.put(self.url(1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unregister_error(self):
        response = self.client.delete(self.url(1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ViewerListTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda(full=True))
        self.viewer = create_viewer(self.agenda, factory.viewer())
        self.url = self.viewer.get_absolute_url()
        self.sessions = [create_session(self.agenda, factory.session(full=True)) for i in range(10)]

    def test_list_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('session', response.data)

    def test_list_full(self):
        indices = [3, 6, 9, 4]

        for i, n in enumerate(indices):
            session = self.sessions[n]
            Registration.objects.create(session=session, viewer=self.viewer)
            response = self.client.get(self.url)
            self.assertEqual(i+1, len(response.data['sessions']))
            self.assertIn(session.pk, response.data['sessions'])

    def test_patch(self):
        viewer_data = factory.viewer(full=True)
        response = self.client.patch(self.url, viewer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(viewer_data['mobile'], response.data['mobile'])
        self.assertEqual(viewer_data['email'], response.data['email'])

    def test_put(self):
        viewer_data = factory.viewer(full=True)
        Registration.objects.create(session=self.sessions[0], viewer=self.viewer)
        response = self.client.put(self.url, viewer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.viewer.refresh_from_db()
        self.assertEqual(viewer_data['mobile'], self.viewer.mobile)
        self.assertEqual(viewer_data['email'], self.viewer.email)
        self.assertTrue(self.viewer.sessions.count())
