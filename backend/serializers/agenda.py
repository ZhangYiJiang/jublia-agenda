from django.db.models import F
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError

from backend.models import Agenda
from .base import BaseSerializer
from .session import SessionSerializer
from .speaker import BaseSpeakerSerializer
from .track import BaseTrackSerializer
from .venue import BaseVenueSerializer


class BaseAgendaSerializer(BaseSerializer):
    def validate_name(self, value):
        profile = self.context['user'].profile
        if profile.agenda_set.filter(name__iexact=value).exists():
            raise ValidationError(_("You already have an event with the name %s" % value))
        return value

    def validate_start_at(self, value):
        if value <= timezone.now().date():
            raise ValidationError(_("The event start date must be later than today"))
        return value

    def validate_duration(self, value):
        # Check if any sessions will be cut off by the duration
        if self.instance:
            minutes = value * 24 * 60
            end_at = F('start_at') + F('duration')
            count = self.instance.session_set.annotate(end_at=end_at)\
                .filter(end_at__gte=minutes).count()
            if count:
                raise ValidationError(_("%d sessions will be cut off by the change in duration" % count))
        return value

    def create_tracks(self, agenda):
        if self.context['tracks']:
            tracks = [{'name': name} for name in self.context['tracks']]
        else:
            tracks = [{}]

        for track in tracks:
            serializer = BaseTrackSerializer(data=track, context={'agenda': agenda})
            serializer.is_valid(True)
            serializer.save()

    @atomic
    def create(self, validated_data):
        validated_data['profile'] = self.context['user'].profile
        agenda = super().create(validated_data)
        self.create_tracks(agenda)
        return agenda

    class Meta:
        model = Agenda
        fields = ('id', 'name', 'location', 'description', 'published',
                  'start_at', 'end_at', 'duration',)


class AgendaSerializer(BaseAgendaSerializer):
    sessions = SessionSerializer(many=True, required=False, source='session_set')
    tracks = BaseTrackSerializer(many=True, required=False, source='track_set')
    speakers = BaseSpeakerSerializer(many=True, required=False, source='speaker_set')
    session_venues = BaseVenueSerializer(many=True, required=False, source='venue_set')

    class Meta:
        model = Agenda
        fields = ('id', 'name', 'location', 'start_at', 'description', 'published', 'end_at',
                  'sessions', 'tracks', 'speakers', 'session_venues', 'duration',)
