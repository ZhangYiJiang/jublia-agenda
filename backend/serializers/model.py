from django.db.transaction import atomic

from backend.models import Track, Speaker, Venue
from .session import SessionSerializer
from .speaker import BaseSpeakerSerializer
from .track import BaseTrackSerializer
from .venue import BaseVenueSerializer


class MarkSessionDirtyMixin:
    @atomic
    def update(self, instance, validated_data):
        updated = super().update(instance, validated_data)
        updated.session_set.filter(agenda__published=True).update(is_dirty=True)
        return updated


class TrackSerializer(BaseTrackSerializer):
    sessions = SessionSerializer(many=True, required=False, source='session_set')

    class Meta:
        model = Track
        fields = ('id', 'name', 'sessions',)


class SpeakerSerializer(MarkSessionDirtyMixin, BaseSpeakerSerializer):
    sessions = SessionSerializer(many=True, required=False, source='session_set')

    class Meta:
        model = Speaker
        fields = ('id', 'name', 'profile', 'company', 'position', 'email', 'phone_number',
                  'company_description', 'company_url', 'sessions', 'image',)


class VenueSerializer(MarkSessionDirtyMixin, BaseVenueSerializer):
    sessions = SessionSerializer(many=True, required=False, source='session_set')

    class Meta:
        model = Venue
        fields = ('id', 'name', 'unit', 'sessions',)
