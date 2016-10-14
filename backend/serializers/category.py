from django.db.transaction import atomic
from rest_framework.relations import StringRelatedField

from backend.models import Category
from backend.serializers.base import BaseSerializer


class CategorySerializer(BaseSerializer):
    tags = StringRelatedField(many=True)

    @atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        category = super().create(validated_data)
        return self._update_tags(category, tags)

    @atomic
    def update(self, instance, validated_data):
        self._update_tags(instance, validated_data.pop('tags', []))
        return super().update(instance, validated_data)

    @staticmethod
    def _update_tags(category, tags):
        category.sync_tags(tags)

    class Meta:
        model = Category
        fields = ('name', 'tags',)