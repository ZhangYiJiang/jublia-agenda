from rest_framework.serializers import ModelSerializer

from backend.models import Agenda
from backend.serializers.session import SessionSerializer


class AgendaSerializer(ModelSerializer):
    sessions = SessionSerializer(many=True, required=False)

    def create(self, validated_data):
        validated_data['profile'] = self.context['user'].profile
        return super().create(validated_data)

    class Meta:
        model = Agenda
        fields = ['name', 'location', 'date', 'sessions', ]
