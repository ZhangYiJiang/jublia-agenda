from rest_framework.serializers import ModelSerializer

from backend.models import Agenda
from backend.serializers.session import SessionSerializer


class AgendaSerializer(ModelSerializer):
    sessions = SessionSerializer(many=True, required=False)

    class Meta:
        model = Agenda
        fields = ['name', 'location', 'date', 'sessions', ]
