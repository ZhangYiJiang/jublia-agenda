from backend.models import Venue
from .base import BaseSerializer


class BaseVenueSerializer(BaseSerializer):
    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    class Meta:
        model = Venue
        fields = ('id', 'name', 'unit',)
