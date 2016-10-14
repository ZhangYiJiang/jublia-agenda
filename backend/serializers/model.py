from backend.models import Track, Speaker
from .session import SessionViewSerializer, SessionUpdateSerializer
from .speaker import BaseSpeakerSerializer
from .track import BaseTrackSerializer


class TrackSerializer(BaseTrackSerializer):
    sessions = SessionViewSerializer(many=True, required=False, source='session_set')

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