from backend.models import Track, Speaker
from .session import SessionUpdateSerializer
from .speaker import BaseSpeakerSerializer
from .track import BaseTrackSerializer
from .venue import BaseVenueSerializer


class TrackSerializer(BaseTrackSerializer):
    sessions = SessionUpdateSerializer(many=True, required=False, source='session_set')

    class Meta:
        model = Track
        fields = ('id', 'name', 'sessions',)


class SpeakerSerializer(BaseSpeakerSerializer):
    sessions = SessionUpdateSerializer(many=True, required=False, source='session_set')

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
    sessions = SessionUpdateSerializer(many=True, required=False, source='session_set')

    class Meta:
        model = Track
        fields = ('id', 'name', 'unit', 'sessions',)
