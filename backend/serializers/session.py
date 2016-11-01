from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from rest_framework.relations import PrimaryKeyRelatedField

from backend.models import Session, Tag
from .base import BaseSerializer, AgendaPrimaryKeyRelatedField, HideFieldsMixin


class DefaultTrack:
    def set_context(self, field):
        self.agenda = field.context['agenda']

    def __call__(self, *args, **kwargs):
        return self.agenda.track_set.first()


class TagPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        return Tag.objects.filter(category__agenda=self.context['agenda'])


class SessionSerializer(HideFieldsMixin, BaseSerializer):
    track = AgendaPrimaryKeyRelatedField(klass='Track', default=DefaultTrack())
    speakers = AgendaPrimaryKeyRelatedField(many=True, required=False, klass='Speaker')
    venue = AgendaPrimaryKeyRelatedField(required=False, klass='Venue')
    tags = TagPrimaryKeyRelatedField(many=True, required=False)

    duration = IntegerField(required=False, allow_null=True, validators=[
        MinValueValidator(1, _("Duration must be larger than zero")),
        MaxValueValidator(24 * 60, _("A session cannot be longer than 24 hours long")),
    ])

    def validate(self, attrs):
        no_duration = 'duration' not in attrs and (not self.instance or 'duration' not in self.instance)
        if 'start_at' in attrs and no_duration:
            raise ValidationError(_("Start time can only be added when the duration is defined"))
        return attrs

    def create(self, validated_data):
        validated_data['agenda'] = self.context['agenda']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self.context['agenda'].published:
            instance.is_dirty = True
        return super().update(instance, validated_data)

    class Meta:
        model = Session
        fields = ('id', 'name', 'description', 'start_at', 'duration', 'speakers', 'track',
                  'venue', 'categories', 'tags', 'popularity', 'is_dirty')
        hidden_fields = ('tags',)
