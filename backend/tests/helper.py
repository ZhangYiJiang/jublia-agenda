from backend.serializers import UserSerializer, AgendaSerializer, SessionSerializer


def create_user(data):
    s = UserSerializer(data=data)
    s.is_valid(raise_exception=True)
    return s.save()


def create_agenda(user, data):
    s = AgendaSerializer(data=data, context={'user': user})
    s.is_valid(True)
    return s.save()


def create_session(agenda, data):
    s = SessionSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()
