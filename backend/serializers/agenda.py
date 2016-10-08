from backend.models import Agenda
from .base import BaseSerializer
from .session import SessionViewSerializer


class AgendaSerializer(BaseSerializer):
    sessions = SessionViewSerializer(many=True, required=False)

    def create(self, validated_data):
        validated_data['profile'] = self.context['user'].profile
        return super().create(validated_data)

    class Meta:
        model = Agenda
        fields = ('id', 'name', 'location', 'date', 'sessions',)
