from rest_framework.fields import ImageField

from backend.models import Attachment
from .base import BaseSerializer


class AttachmentSerializer(BaseSerializer):
    file = ImageField()

    def create(self, validated_data):
        validated_data['profile'] = self.context['request'].user.profile
        return super().create(validated_data)

    class Meta:
        model = Attachment
        fields = ('id', 'file',)
