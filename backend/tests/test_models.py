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
        self.track = Track.objects.create(agenda=self.agenda)

    def create_session(self, start, duration):
        return Session.objects.create(agenda=self.agenda, **factory.session(data={
            'start_at': start,
            'duration': duration,
            'track': self.track,
        }))

    def test_end_at_sessions(self):
        self.assertIsNone(self.agenda.end_at)

        # Create some session and check that the end date for the last
        self.agenda.start_at = factory.today
        for i in range(6):
            self.create_session(24 * 60 * i, 60)
        self.create_session(24 * 60 * 6, 120)
        Session.objects.create(agenda=self.agenda, track=self.track, **factory.session())

        self.assertEqual(self.agenda.end_at, factory.today + timedelta(minutes=24 * 60 * 6 + 120))

    def test_end_at_duration(self):
        self.agenda.duration = 4
        self.assertIsNone(self.agenda.end_at)
        self.agenda.start_at = factory.today
        self.assertEqual(self.agenda.end_at, factory.today + timedelta(days=4))


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


class SessionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(**factory.user())
        self.profile = Profile.objects.create(user=self.user)
        self.agenda = Agenda.objects.create(profile=self.profile, name='Test')
        self.track = Track.objects.create(agenda=self.agenda)

    def test_default_sort(self):
        for i in range(5):
            Session.objects.create(**factory.session(full=True, data={
                'agenda': self.agenda,
                'track': self.track,
            }))

        last = Session.objects.first()
        for session in Session.objects.all()[1:]:
            self.assertGreater(session.start_at, last.start_at)
            last = session
