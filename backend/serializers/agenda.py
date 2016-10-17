from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError

from backend.models import Agenda
from .base import BaseSerializer
from .session import SessionUpdateSerializer
from .speaker import BaseSpeakerSerializer
from .track import BaseTrackSerializer
from .venue import BaseVenueSerializer


class BaseAgendaSerializer(BaseSerializer):
    def validate_start_at(self, value):
        if value <= timezone.now().date():
            raise ValidationError(_("The event start date must be later than today"))
        return value

    @atomic
    def create(self, validated_data):
        validated_data['profile'] = self.context['user'].profile
        agenda = super().create(validated_data)
        # Create a default track for the new agenda
        track = BaseTrackSerializer(data={}, context={'agenda': agenda})
        track.is_valid(True)
        track.save()
        return agenda

    class Meta:
        model = Agenda
        fields = ('id', 'name', 'location', 'description', 'start_at', 'end_at', 'duration',)


class AgendaSerializer(BaseAgendaSerializer):
    sessions = SessionUpdateSerializer(many=True, required=False, source='session_set')
    tracks = BaseTrackSerializer(many=True, required=False, source='track_set')
    speakers = BaseSpeakerSerializer(many=True, required=False, source='speaker_set')
    venues = BaseVenueSerializer(many=True, required=False, source='venue_set')

    class Meta:
        model = Agenda
        fields = ('id', 'name', 'location', 'start_at', 'description', 'end_at', 'sessions', 'tracks',
                  'speakers', 'venues', 'duration',)
