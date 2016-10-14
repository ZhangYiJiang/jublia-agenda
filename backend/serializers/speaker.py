from backend.models import Speaker
from .base import BaseSerializer
from .session import SessionUpdateSerializer


class BaseSpeakerSerializer(BaseSerializer):
    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Speaker
        fields = ('id', 'name', 'company', 'position', 'email', 'phone_number', 'company_description', 'company_url',)


class SpeakerSerializer(BaseSpeakerSerializer):
    sessions = SessionUpdateSerializer(many=True, required=False, source='session_set')

    class Meta:
        model = Speaker
        fields = ('id', 'name', 'company', 'position', 'email', 'phone_number', 'company_description', 'company_url', 'sessions',)
