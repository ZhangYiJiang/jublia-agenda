from collections import defaultdict
from datetime import timedelta, datetime, time

from django.conf import settings
from django.db import models
from django.utils import timezone
from icalendar import Event
from rest_framework.reverse import reverse

from .agenda import Agenda
from .base import BaseModel
from .session_meta import Track, Venue
from .speaker import Speaker


class Tag(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', models.CASCADE)

    def get_absolute_url(self):
        return reverse('tag-detail', [self.category.agenda.pk, self.category.pk, self.pk])

    def __str__(self):
        return self.name


class Session(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_at = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    # Denormalized aggregate of the number of registrations on the model
    popularity = models.IntegerField(default=0, editable=False)

    is_dirty = models.BooleanField(default=False, editable=False)

    agenda = models.ForeignKey(Agenda, models.CASCADE)
    tags = models.ManyToManyField(Tag)
    speakers = models.ManyToManyField(Speaker)
    track = models.ForeignKey(Track, models.CASCADE)
    venue = models.ForeignKey(Venue, models.SET_NULL, blank=True, null=True)

    @property
    def categories(self):
        categories = defaultdict(list)
        for category, tag in self.tags.values_list('category__pk', 'pk'):
            categories[category].append(tag)
        return categories

    def timestamps(self):
        if not self.duration or not self.agenda.start_at:
            return None
        start = datetime.combine(self.agenda.start_at, time.min) + timedelta(minutes=self.start_at)
        return start, start + timedelta(minutes=self.duration)

    def to_ical(self):
        start, end = self.timestamps()
        if not end:
            raise ValueError

        cal = Event()
        cal.add('uid', str(self.pk) + settings.ICAL_UID_SUFFIX)
        cal.add('dtstart', start)
        cal.add('dtend', end)
        cal.add('dtstamp', timezone.now())
        cal.add('summary', self.name)
        if self.description:
            cal.add('description', self.description)

        return cal

    def get_absolute_url(self):
        return reverse('session_detail', (self.agenda.pk, self.pk,))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('start_at',)


class Category(BaseModel):
    name = models.CharField(max_length=255)
    agenda = models.ForeignKey(Agenda, models.CASCADE)

    def add_tags(self, tags):
        """
        Adds any new tags in the list of strings to this category
        :param tags An iterable of tags represented by strings. Duplicates will be ignored
        """
        tags = set(tags)
        existing = set(t.name for t in self.tag_set.all())
        Tag.objects.bulk_create([Tag(name=name, category=self) for name in tags - existing])

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
        Tag.objects.bulk_create([Tag(name=name, category=self) for name in tags - existing])

    def get_absolute_url(self):
        return reverse('category-detail', [self.agenda.pk, self.pk])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
