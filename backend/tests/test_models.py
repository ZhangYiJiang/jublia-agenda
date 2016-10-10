from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from backend.models import *
from . import factory


class AgendaTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(**factory.user())
        self.profile = Profile.objects.create(user=self.user)
        self.agenda = Agenda.objects.create(profile=self.profile, name='Test')

    def create_session(self, start, duration):
        return Session.objects.create(agenda=self.agenda, **factory.session(data={
            'start_at': start,
            'duration': duration,
        }))

    def test_end_at(self):
        self.assertIsNone(self.agenda.end_at)

        # Create some session and check that the end date for the last
        self.agenda.start_at = factory.today
        for i in range(6):
            self.create_session(24 * 60 * i, 60)
        self.create_session(24 * 60 * 6, 120)

        self.assertEqual(self.agenda.end_at, factory.today + timedelta(minutes=24 * 60 * 6 + 120))


class CategoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(**factory.user())
        self.profile = Profile.objects.create(user=self.user)
        self.agenda = Agenda.objects.create(profile=self.profile, **factory.agenda())
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

