from backend.serializers import UserSerializer, AgendaSerializer, SessionUpdateSerializer
from backend.serializers.speaker import SpeakerSerializer


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
