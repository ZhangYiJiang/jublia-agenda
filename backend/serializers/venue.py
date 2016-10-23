from rest_framework.fields import CharField

from backend.models import Venue
from .base import BaseSerializer, UniqueForAgenda


class BaseVenueSerializer(BaseSerializer):
    name = CharField(validators=[UniqueForAgenda(queryset=Venue.objects.all())])

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Venue
        fields = ('id', 'name', 'unit',)
