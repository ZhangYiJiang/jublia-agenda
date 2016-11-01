from backend.models import Speaker
from backend.serializers.attachment import AttachmentField
from .base import BaseSerializer, unique_for_agenda


class BaseSpeakerSerializer(BaseSerializer):
    validate_name = unique_for_agenda('name')
    image = AttachmentField(required=False)

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Speaker
        fields = ('id', 'name', 'profile', 'company', 'position', 'email',
                  'phone_number', 'company_description', 'company_url', 'image',)
