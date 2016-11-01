from rest_framework.fields import ImageField

from backend.models import Attachment
from .base import BaseSerializer


class FileSerializer(BaseSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'file',)


class ImageSerializer(BaseSerializer):
    file = ImageField()

    class Meta:
        model = Attachment
        fields = ('id', 'file',)
