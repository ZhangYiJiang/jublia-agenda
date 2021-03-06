import random

from django.core.management import BaseCommand

from backend.tests import factory
from backend.tests.helper import *


def during_working_hours(start_at):
    return 9 <= (start_at / 60) % 24 <= 16


def coin():
    return random.choice([True, False])


def full_session(tracks, speakers, venues):
    return factory.session(full=True, data={
        'track': random.choice(tracks).pk,
        'venue': random.choice(venues).pk,
        'speakers': [random.choice(speakers).pk],
    })


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--user')
        parser.add_argument('--tracks', type=int, default=2)
        parser.add_argument('--sessions', type=int, default=20)
        parser.add_argument('--speakers', type=int, default=5)
        parser.add_argument('--venues', type=int, default=3)

    def out(self, output):
        self.stdout.write(self.style.SUCCESS(output))

    def handle(self, *args, **options):
        if options['user']:
            user = User.objects.get(username=options['user'])
        else:
            user_data = factory.user(full=True)
            user = create_user(user_data)
            self.out('Username: ' + user_data['username'])
            self.out('Password: ' + user_data['password'])

        agenda_data = factory.agenda(full=True)
        agenda = create_agenda(user, agenda_data)
        self.out('Creating event: ' + agenda_data['name'])

        tracks = [agenda.track_set.first()]
        speakers = []
        sessions = []
        venues = []

        for i in range(options['tracks'] - 1):  # minus one because a default track is created with agenda
            tracks.append(create_track(agenda))

        for i in range(options['speakers']):
            speakers.append(create_speaker(agenda, factory.speaker(full=coin())))

        for i in range(options['venues']):
            venues.append(create_venue(agenda, factory.venue(full=True)))

        for i in range(options['sessions']):
            if coin():
                session_data = factory.session()
                sessions.append(create_session(agenda, session_data))
            else:
                session_data = full_session(tracks, speakers, venues)
                while not during_working_hours(session_data['start_at']):
                    session_data = full_session(tracks, speakers, venues)
                sessions.append(create_session(agenda, session_data))
            self.out('Creating session: ' + session_data['name'])
