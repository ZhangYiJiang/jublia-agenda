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

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Viewer
        fields = ('email', 'sessions',)
