from rest_framework.serializers import ModelSerializer, StringRelatedField
from django.db.transaction import atomic

from backend.models import Session, Category


class CategorySerializer(ModelSerializer):
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


class SessionSerializer(ModelSerializer):
    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Session
        fields = ('name', 'description', 'start_at', 'end_at',)
