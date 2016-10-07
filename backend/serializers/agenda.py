from backend.models import Agenda
from .base import BaseSerializer
from .session import SessionSerializer


class AgendaSerializer(BaseSerializer):
    sessions = SessionSerializer(many=True, required=False)

    def create(self, validated_data):
        validated_data['profile'] = self.context['user'].profile
        return super().create(validated_data)

    class Meta:
        model = Agenda
        fields = ['name', 'location', 'date', 'sessions', ]
