from django.contrib.auth.models import User

from backend.serializers import UserSerializer, AgendaSerializer
from backend.tests import data


def create_user(data):
    s = UserSerializer(data=data)
    s.is_valid(raise_exception=True)
    return s.save()


def create_default_user():
    user = User.objects.filter(email=data.user['email']).first()
    if user:
        return user
    return create_user(data.user)


def create_agenda(data):
    user = create_default_user()
    s = AgendaSerializer(data=data, context={'user': user})
    s.is_valid(True)
    return s.save()


def create_default_agenda():
    return create_agenda(data.agenda)