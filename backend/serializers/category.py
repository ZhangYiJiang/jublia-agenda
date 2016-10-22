from django.db.transaction import atomic

from backend.models import Category, Tag
from backend.serializers.base import BaseSerializer


class TagSerializer(BaseSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


class CategorySerializer(BaseSerializer):
    tags = TagSerializer(many=True, required=False)

    def validate_tags(self, tags):
        return [{'name': name} for name in tags]

    @atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        category = super().create(validated_data)
        category.sync_tags(tags)
        return category

    def update(self, instance, validated_data):
        # Update does not accept the setting of tags
        validated_data.pop('tags', [])
        return super().update(instance, validated_data)

    class Meta:
        model = Category
        fields = ('id', 'name', 'tags',)
