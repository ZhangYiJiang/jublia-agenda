from backend.models import Registration
from backend.models import Viewer
from .base import BaseSerializer, AgendaPrimaryKeyRelatedField


class RegistrationSerializer(BaseSerializer):
    viewer = AgendaPrimaryKeyRelatedField(klass='viewer')
    session = AgendaPrimaryKeyRelatedField(klass='session')

    class Meta:
        model = Registration
        fields = ('viewer', 'session',)


class ViewerSerializer(BaseSerializer):
    sessions = AgendaPrimaryKeyRelatedField(klass='session', many=True, required=False)

    class Meta:
        model = Viewer
        fields = ('email', 'sessions',)
