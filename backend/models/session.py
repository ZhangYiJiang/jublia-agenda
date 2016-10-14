from django.db import models
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from backend.models.speaker import Speaker
from .agenda import Agenda
from .base import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category')

    def __str__(self):
        return self.name


class Track(BaseModel):
    name = models.CharField(max_length=120)
    agenda = models.ForeignKey(Agenda)

    def get_absolute_url(self):
        return reverse('track_detail', args=(self.agenda.pk, self.pk,))

    @atomic
    def delete(self, using=None, keep_parents=False):
        if self.agenda.track_set.count() == 1:
            raise ValidationError("The event agenda must have at least one track")

        # Move all existing sessions on this track to another one to prevent the
        # delete from cascading to them
        self.session_set.update(track=self.agenda.track_set.exclude(pk=self.pk).first())

        super().delete(using, keep_parents)

    def __str__(self):
        return self.name


class Session(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_at = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    agenda = models.ForeignKey(Agenda)
    tags = models.ManyToManyField(Tag)
    speakers = models.ManyToManyField(Speaker)
    track = models.ForeignKey(Track)

    @property
    def owner(self):
        return self.agenda.owner

    def get_absolute_url(self):
        return reverse('session_detail', (self.agenda.pk, self.pk,))

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=255)
    agenda = models.ForeignKey(Agenda)

    def add_tags(self, tags):
        """
        Adds any new tags in the list of strings to this category
        :param tags An iterable of tags represented by strings. Duplicates will be ignored
        """
        tags = set(tags)
        existing = set(t.name for t in self.tag_set.all())
        for name in tags - existing:
            self.tag_set.add(Tag.objects.create(name=name, category=self))

    def sync_tags(self, tags):
        """
        Synchronizes (replaces) tags on this category
        :param tags An iterable of tags represented by strings. Duplicates will be ignored
        """
        tags = set(tags)
        existing = set(t.name for t in self.tag_set.all())
        # Delete tags that does not appear in the new tag list
        self.tag_set.filter(name__in=existing - tags).delete()
        # Add tags which didn't exist before
        for name in tags - existing:
            self.tag_set.add(Tag.objects.create(name=name, category=self))

    def __str__(self):
        return self.name
