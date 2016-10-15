from rest_framework.exceptions import ValidationError

from backend.models import Session
from .base import BaseSerializer, AgendaPrimaryKeyRelatedField
from .speaker import BaseSpeakerSerializer
from .track import BaseTrackSerializer
from .venue import BaseVenueSerializer


class DefaultTrack:
    def set_context(self, field):
        self.agenda = field.context['agenda']

    def __call__(self, *args, **kwargs):
        return self.agenda.track_set.first()


class SessionViewSerializer(BaseSerializer):
    track = BaseTrackSerializer()
    speakers = BaseSpeakerSerializer(many=True)
    venue = BaseVenueSerializer()

    class Meta:
        model = Session
        fields = ('id', 'name', 'description', 'start_at', 'duration', 'speakers', 'track', 'venue',)


class SessionUpdateSerializer(BaseSerializer):
    track = AgendaPrimaryKeyRelatedField(klass='Track', default=DefaultTrack())
    speakers = AgendaPrimaryKeyRelatedField(many=True, required=False, klass='Speaker')
    venue = AgendaPrimaryKeyRelatedField(required=False, klass='Venue')

    def validate(self, attrs):
        if 'start_at' in attrs and 'duration' not in attrs and 'duration' not in self.instance:
            raise ValidationError("Start time can only be added when the duration is defined")
        return attrs

    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Session duration can't be less than or equal to zero")
        return value

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Session
        fields = ('id', 'name', 'description', 'start_at', 'duration', 'speakers', 'track', 'venue',)
