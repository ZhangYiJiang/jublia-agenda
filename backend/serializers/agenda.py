from django.db.transaction import atomic

from backend.models import Agenda
from .base import BaseSerializer
from .session import SessionViewSerializer
from .track import TrackSerializer


class AgendaSerializer(BaseSerializer):
    sessions = SessionViewSerializer(many=True, required=False)

    @atomic
    def create(self, validated_data):
        validated_data['profile'] = self.context['user'].profile
        agenda = super().create(validated_data)
        # Create a default track for the new agenda
        track = TrackSerializer(data={}, context={'agenda': agenda})
        track.is_valid(True)
        track.save()
        return agenda

    class Meta:
        model = Agenda
        fields = ('id', 'name', 'location', 'start_at', 'sessions',)
