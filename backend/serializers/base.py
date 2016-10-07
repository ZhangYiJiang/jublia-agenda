from collections import OrderedDict

from rest_framework.serializers import ModelSerializer


class BaseSerializer(ModelSerializer):
    def to_representation(self, instance):
        obj = super().to_representation(instance)

        # Add URL field for objects with URL
        try:
            obj['url'] = instance.get_absolute_url()
        except (AttributeError, TypeError):
            pass

        # Filter out empty strings and other stuff
        filtered_obj = OrderedDict()
        for key, value in obj.items():
            try:
                if len(value):
                    filtered_obj[key] = value
            except TypeError:
                filtered_obj[key] = value

        return filtered_obj

    def update(self, instance, validated_data):
        # For non-partial (PUT) requests, reset to initial any fields
        # which are not present in the request
        if not self.partial:
            for name, field in self.fields.items():
                if name not in validated_data:
                    validated_data[name] = field.initial
        return super().update(instance, validated_data)


class HideFieldsMixin:
    def to_representation(self, instance):
        obj = super().to_representation(instance)
        if hasattr(self.Meta, 'hidden_fields'):
            for f in self.Meta.hidden_fields:
                obj.pop(f, None)
        return obj
