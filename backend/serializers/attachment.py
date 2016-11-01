from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from backend.models import Attachment
from .base import BaseSerializer


class AttachmentField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return get_object_or_404(self.context['request'].user.profile.attachment_set, pk=data)


class AttachmentSerializer(BaseSerializer):
    def create(self, validated_data):
        validated_data['profile'] = self.context['request'].user.profile
        return super().create(validated_data)

    class Meta:
        model = Attachment
        fields = ('id', 'file',)
