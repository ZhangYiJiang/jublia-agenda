from rest_framework.exceptions import ValidationError

from backend.models import Session
from .base import BaseSerializer, AgendaPrimaryKeyRelatedField
from .speaker import SpeakerSerializer
from .track import TrackSerializer


class DefaultTrack:
    def set_context(self, field):
        self.agenda = field.context['agenda']

    def __call__(self, *args, **kwargs):
        return self.agenda.track_set.first()


class SessionViewSerializer(BaseSerializer):
    speakers = SpeakerSerializer(many=True, required=False)

    class Meta:
        model = Session
        fields = ('id', 'name', 'description', 'start_at', 'duration', 'speakers',)


class SessionUpdateSerializer(BaseSerializer):
    track = TrackSerializer(default=DefaultTrack())
    speakers = AgendaPrimaryKeyRelatedField(many=True, required=False, klass='Speaker')

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
        fields = ('id', 'name', 'description', 'start_at', 'duration', 'speakers', 'track',)
