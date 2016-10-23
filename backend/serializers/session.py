from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError

from backend.models import Session
from .base import BaseSerializer, AgendaPrimaryKeyRelatedField


class DefaultTrack:
    def set_context(self, field):
        self.agenda = field.context['agenda']

    def __call__(self, *args, **kwargs):
        return self.agenda.track_set.first()


class SessionSerializer(BaseSerializer):
    track = AgendaPrimaryKeyRelatedField(klass='Track', default=DefaultTrack())
    speakers = AgendaPrimaryKeyRelatedField(many=True, required=False, klass='Speaker')
    venue = AgendaPrimaryKeyRelatedField(required=False, klass='Venue')

    def validate(self, attrs):
        no_duration = 'duration' not in attrs and (not self.instance or 'duration' not in self.instance)
        if 'start_at' in attrs and no_duration:
            raise ValidationError(_("Start time can only be added when the duration is defined"))
        return attrs

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Session
        fields = ('id', 'name', 'description', 'start_at', 'duration', 'speakers', 'track',
                  'venue', 'categories', 'popularity',)
        unique_together = ('agenda', 'name',)
