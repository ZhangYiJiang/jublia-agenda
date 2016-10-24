from backend.models import Venue
from .base import BaseSerializer, unique_for_agenda


class BaseVenueSerializer(BaseSerializer):
    validate_name = unique_for_agenda('name')

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Venue
        fields = ('id', 'name', 'unit',)
