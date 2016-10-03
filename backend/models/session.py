from django.db import models
from .base import BaseModel
from .agenda import Agenda


class Tag(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category')

    def __str__(self):
        return self.name


class Session(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    agenda = models.ForeignKey(Agenda)
    tags = models.ManyToManyField(Tag)

    @property
    def owner(self):
        return self.agenda.owner

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
