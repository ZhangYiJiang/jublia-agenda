from django.core.validators import MinValueValidator
from django.db.models import F
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField

from backend.models import Agenda
from .base import BaseSerializer
from .category import CategorySerializer
from .session import SessionSerializer
from .speaker import BaseSpeakerSerializer
from .track import BaseTrackSerializer
from .venue import BaseVenueSerializer

DEFAULT_CATEGORY = 'Tags'


class BaseAgendaSerializer(BaseSerializer):
    duration = IntegerField(default=3, validators=[
        MinValueValidator(1, _("The duration of the event must be at least one day long")),
    ])

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
        if self.context.get('tracks', False):
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
        agenda.category_set.create(name=DEFAULT_CATEGORY)
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
    categories = CategorySerializer(many=True, required=False, source='category_set')

    class Meta:
        model = Agenda
        fields = ('id', 'name', 'location', 'start_at', 'description', 'published', 'end_at',
                  'categories', 'sessions', 'tracks', 'speakers', 'session_venues', 'duration',)
