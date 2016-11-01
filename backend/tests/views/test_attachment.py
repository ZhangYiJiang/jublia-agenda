import os

from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import create_user
from .base import BaseAPITestCase


def resource(filename):
    return os.path.dirname(os.path.abspath(__file__)) + '/../resource/' + filename


class UploadFileTest(BaseAPITestCase):
    url = reverse('upload-image')

    def setUp(self):
        self.user = create_user(factory.user())

    def try_upload(self, file):
        self.login(self.user)
        with open(resource(file), 'rb') as fp:
            return self.client.post(self.url, {'file': fp}, format='multipart')

    def test_upload_image(self):
        response = self.try_upload('kitten.jpg')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_upload_non_image(self):
        response = self.try_upload('file.js')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated(self):
        self.assert401WhenUnauthenticated(self.url)
