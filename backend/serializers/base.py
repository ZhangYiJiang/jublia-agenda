from rest_framework.serializers import ModelSerializer


class BaseSerializer(ModelSerializer):
    def to_representation(self, instance):
        obj = super().to_representation(instance)
        try:
            obj['url'] = instance.get_absolute_url()
        except (AttributeError, TypeError):
            pass
        return obj


class HideFieldsMixin:
    def to_representation(self, instance):
        obj = super().to_representation(instance)
        if hasattr(self.Meta, 'hidden_fields'):
            for f in self.Meta.hidden_fields:
                obj.pop(f, None)
        return obj
