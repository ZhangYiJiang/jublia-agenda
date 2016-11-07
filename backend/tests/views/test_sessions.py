from random import randint

from rest_framework import status
from rest_framework.reverse import reverse

from backend.tests import factory
from backend.tests.helper import *
from .base import BaseAPITestCase, DetailAuthTestMixin, ListAuthTestMixin


class SessionListTest(ListAuthTestMixin, BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.url = reverse('session_list', args=[self.agenda.pk])

    def test_list(self):
        create_session(self.agenda, factory.session())
        create_session(self.agenda, factory.session(full=True))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

        # Check that relations are represented with IDs
        track = self.agenda.track_set.first()
        self.assertEqual(response.data[0]['tracks'], [track.pk])

    def test_list_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, len(response.data))

    def test_create(self):
        self.login(self.user)
        response = self.client.post(self.url, factory.session())
        self.assertCreatedOk(response)
        # Should be automatically assigned to a track when created
        self.assertEqual(self.agenda.track_set.first().pk, response.data['tracks'][0])

    def test_create_full(self):
        self.login(self.user)

        # Create multiple tracks, speakers and category tags to test against
        tracks = [create_track(self.agenda) for i in range(3)]
        speakers = [
            create_speaker(self.agenda, factory.speaker()),
            create_speaker(self.agenda, factory.speaker(full=True)),
        ]
        category = create_category(self.agenda, factory.category(), ['A', 'B', 'C'])
        venue = create_venue(self.agenda, factory.venue(full=True))

        session_data = factory.session(full=True, data={
            'speakers': [s.pk for s in speakers],
            'tracks': [t.pk for t in tracks],
            'tags': [t.pk for t in category.tag_set.all()],
            'venue': venue.pk,
        })

        response = self.client.post(self.url, session_data)

        self.assertCreatedOk(response)
        self.assertEqual(response.data['venue'], venue.pk)
        # Check that the speakers and tracks match, and that the session's
        # many-to-many relationships have been created
        pk = response.data['id']
        for track in tracks:
            self.assertTrue(track.session_set.filter(pk=pk).exists())
            self.assertIn(track.pk, response.data['tracks'])

        for speaker in speakers:
            self.assertTrue(speaker.session_set.filter(pk=pk).exists())
            self.assertIn(speaker.pk, response.data['speakers'])

        # Tags are represented as categories but received as arrays
        session_data.pop('tags')
        for tag in category.tag_set.all():
            self.assertTrue(tag.session_set.filter(pk=pk).exists())
            self.assertIn(tag.pk, response.data['categories'][category.pk])

        self.assertEqualExceptMeta(session_data, response.data,
                                   ignore=('popularity', 'categories', 'is_dirty'))


class SessionDetailTest(DetailAuthTestMixin, BaseAPITestCase):
    def assertSessionEqual(self, original, response, msg=None):
        self.assertEqualExceptMeta(original, response, ignore=('tracks', 'popularity', 'is_dirty',))

    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.session_data = factory.session()
        self.session = create_session(self.agenda, self.session_data)
        self.url = self.session.get_absolute_url()

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.session_data['name'])
        self.assertNoEmptyFields(response.data)

        # Check relations
        self.assertIsInstance(response.data['tracks'][0], int)

    def test_speaker(self):
        speaker_data = factory.speaker()
        speaker = create_speaker(self.agenda, speaker_data)
        self.session.speakers.add(speaker)
        response = self.client.get(self.url)
        self.assertEqual(speaker.pk, response.data['speakers'][0])

    def test_venue(self):
        venue_data = factory.venue(full=True)
        venue = create_venue(self.agenda, venue_data)
        self.session.venue = venue
        self.session.save()
        response = self.client.get(self.url)
        self.assertEqual(venue.pk, response.data['venue'])

    def test_category(self):
        category = create_category(self.agenda, factory.category(), ['A', 'B', 'C'])
        tags = category.tag_set.all()
        self.session.tags.add(*tags)
        response = self.client.get(self.url)
        for tag in tags:
            self.assertTrue(tag.pk in response.data['categories'][category.pk])

    def test_delete(self):
        self.login(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch(self):
        self.login(self.user)

        response = self.client.patch(self.url, {
            'name': 'New Conference Name'
        })
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Conference Name')
        self.assertNoEmptyFields(response.data)

        # Test attaching speakers
        speakers = [
            create_speaker(self.agenda, factory.speaker()).pk,
            create_speaker(self.agenda, factory.speaker()).pk,
            create_speaker(self.agenda, factory.speaker()).pk,
        ]
        response = self.client.patch(self.url, {
            'speakers': speakers,
        })
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, len(response.data['speakers']))
        self.assertNoEmptyFields(response.data)

    def test_put(self):
        self.login(self.user)
        data = factory.session(full=True)
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSessionEqual(data, response.data)

        data = factory.session()
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertSessionEqual(data, response.data)


class SessionDirtyTest(BaseAPITestCase):
    def setUp(self):
        self.user = create_user(factory.user())
        self.agenda = create_agenda(self.user, factory.agenda())
        self.sessions = [create_session(self.agenda, factory.session()) for i in range(5)]

    def assertSessionDirtyStatus(self, sessions, status):
        for session in self.sessions:
            session.refresh_from_db()
            self.assertEqual(session.is_dirty, status)

    def assertDirtiness(self, action):
        # Unpublished - will not set to dirty
        self.agenda.published = False
        self.agenda.save()
        action()
        self.assertSessionDirtyStatus(self.sessions, False)

        # Published but with zero popularity - will not set to dirty
        self.agenda.published = True
        self.agenda.save()
        action()
        self.assertSessionDirtyStatus(self.sessions, False)

        # Published and with > 0 popularity - will set to dirty
        for session in self.sessions:
            session.popularity = randint(1, 100)
            session.save()
        action()
        self.assertSessionDirtyStatus(self.sessions, True)

    def test_is_dirty_default(self):
        self.assertFalse(self.sessions[0].is_dirty)

    def test_modify_session(self):
        self.login(self.user)

        def action():
            for session in self.sessions:
                self.client.put(session.get_absolute_url(), factory.session(full=True))
        self.assertDirtiness(action)

    def test_is_dirty_speaker(self):
        self.login(self.user)

        speaker = create_speaker(self.agenda, factory.speaker(full=True))
        for session in self.sessions:
            session.speakers.add(speaker)

        def action():
            self.client.put(speaker.get_absolute_url(), factory.speaker(full=True))
        self.assertDirtiness(action)

    def test_is_dirty_venue(self):
        self.login(self.user)

        venue = create_venue(self.agenda, factory.venue(full=True))
        for session in self.sessions:
            session.venue = venue
            session.save()

        def action():
            self.client.put(venue.get_absolute_url(), factory.venue(full=True))
        self.assertDirtiness(action)
