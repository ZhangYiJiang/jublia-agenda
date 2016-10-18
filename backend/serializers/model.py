from backend.models import Track, Speaker, Venue
from .session import SessionSerializer
from .speaker import BaseSpeakerSerializer
from .track import BaseTrackSerializer
from .venue import BaseVenueSerializer


class TrackSerializer(BaseTrackSerializer):
    sessions = SessionSerializer(many=True, required=False, source='session_set')

    class Meta:
        model = Track
        fields = ('id', 'name', 'sessions',)


class SpeakerSerializer(BaseSpeakerSerializer):
    sessions = SessionSerializer(many=True, required=False, source='session_set')

    class Meta:
        model = Speaker
        fields = (
            'id',
            'name',
            'company',
            'position',
            'email',
            'phone_number',
            'company_description',
            'company_url',
            'sessions',
        )


class VenueSerializer(BaseVenueSerializer):
    sessions = SessionSerializer(many=True, required=False, source='session_set')

    class Meta:
        model = Venue
        fields = ('id', 'name', 'unit', 'sessions',)
