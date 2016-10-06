from django.contrib.auth.models import User

from backend.serializers import UserSerializer, AgendaSerializer, SessionSerializer
from backend.tests import data as test_data


def create_user(data):
    s = UserSerializer(data=data)
    s.is_valid(raise_exception=True)
    return s.save()


def create_default_user():
    user = User.objects.filter(email=test_data.user['email']).first()
    if user:
        return user
    return create_user(test_data.user)


def create_agenda(data):
    user = create_default_user()
    s = AgendaSerializer(data=data, context={'user': user})
    s.is_valid(True)
    return s.save()


def create_default_agenda():
    return create_agenda(test_data.agenda)


def create_session(agenda, data):
    s = SessionSerializer(data=data, context={'agenda': agenda})
    s.is_valid(True)
    return s.save()
