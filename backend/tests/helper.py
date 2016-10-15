from backend.serializers import *


def create_user(data):
    s = UserSerializer(data=data)
    s.is_valid(raise_exception=True)
    return s.save()


def create_agenda(user, data):
    s = AgendaSerializer(data=data, context={'user': user})
    s.is_valid(True)
    return s.save()


def create_session(agenda, data):
    s = SessionUpdateSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()


def create_speaker(agenda, data):
    s = SpeakerSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()


def create_track(agenda, data=None):
    if data is None:
        data = {}
    s = TrackSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()


def create_venue(agenda, data):
    s = VenueSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()
