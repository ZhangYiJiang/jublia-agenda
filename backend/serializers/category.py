from django.db.transaction import atomic
from rest_framework.fields import CharField

from backend.models import Category, Tag
from backend.serializers.base import BaseSerializer, UniqueForAgenda


class TagSerializer(BaseSerializer):
    def create(self, validated_data):
        validated_data['category'] = self.context['category']
        return super().create(validated_data)

    class Meta:
        model = Tag
        fields = ('id', 'name',)


class BaseCategorySerializer(BaseSerializer):
    name = CharField(validators=[UniqueForAgenda(queryset=Category.objects.all())])

    @atomic
    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        category = super().create(validated_data)
        category.add_tags(self.context['tags'])
        return category

    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategorySerializer(BaseCategorySerializer):
    tags = TagSerializer(many=True, required=False, source='tag_set')

    def update(self, instance, validated_data):
        # Update does not accept the setting of tags
        validated_data.pop('tags', [])
        return super().update(instance, validated_data)

    class Meta:
        model = Category
        fields = ('id', 'name', 'tags',)
