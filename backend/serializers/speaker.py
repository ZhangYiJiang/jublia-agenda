from rest_framework.fields import CharField

from backend.models import Speaker
from .base import BaseSerializer, UniqueForAgenda


class BaseSpeakerSerializer(BaseSerializer):
    name = CharField(validators=[UniqueForAgenda(queryset=Speaker.objects.all())])

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Speaker
        fields = ('id', 'name', 'company', 'position', 'email', 'phone_number', 'company_description', 'company_url',)
