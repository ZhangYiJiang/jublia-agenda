from django.db.transaction import atomic

from backend.models import Category, Tag
from backend.serializers.base import BaseSerializer


class TagSerializer(BaseSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


class CreateCategorySerializer(BaseSerializer):
    @atomic
    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        category = super().create(validated_data)
        category.sync_tags(self.context['tags'])
        return category

    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategorySerializer(BaseSerializer):
    tags = TagSerializer(many=True, required=False, source='tag_set')

    def update(self, instance, validated_data):
        # Update does not accept the setting of tags
        validated_data.pop('tags', [])
        return super().update(instance, validated_data)

    class Meta:
        model = Category
        fields = ('id', 'name', 'tags',)
