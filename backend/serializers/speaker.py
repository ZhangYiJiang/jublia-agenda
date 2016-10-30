from backend.models import Speaker
from .base import BaseSerializer, unique_for_agenda


class BaseSpeakerSerializer(BaseSerializer):
    validate_name = unique_for_agenda('name')

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Speaker
        fields = ('id', 'name', 'profile', 'company', 'position', 'email',
                  'phone_number', 'company_description', 'company_url',)
