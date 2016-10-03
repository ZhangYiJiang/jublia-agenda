from django.contrib.auth.models import User
from django.test import TestCase

from backend.models import *
from backend.tests.data import user_data, agenda_data


class CategoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(**user_data)
        self.profile = Profile.objects.create(user=self.user)
        self.agenda = Agenda.objects.create(profile=self.profile, **agenda_data)
        self.category = Category.objects.create(agenda=self.agenda, name='test')

    def assertTagsEqual(self, category, tags, msg=None):
        tags = set(tags)
        self.assertSetEqual(tags, set(category.tag_set.values_list('name', flat=True)), msg)

    def test_sync_tag(self):
        tags = {'a', 'b', 'c'}
        self.category.sync_tags(tags)
        self.assertTagsEqual(self.category, tags)

        tags = {'b', 'c'}
        self.category.sync_tags(tags)
        self.assertTagsEqual(self.category, tags)

        tags = {'c', 'd', 'e'}
        self.category.sync_tags(tags)
        self.assertTagsEqual(self.category, tags)

    def test_add_tag(self):
        tags = {'a', 'b', 'c'}
        self.category.add_tags(tags)
        self.assertTagsEqual(self.category, tags)

        tags |= {'b', 'c'}
        self.category.add_tags(tags)
        self.assertTagsEqual(self.category, tags)

        tags |= {'c', 'd', 'e'}
        self.category.add_tags(tags)
        self.assertTagsEqual(self.category, tags)

