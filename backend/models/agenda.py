from datetime import timedelta

import autoslug.fields
from django.db import models
from rest_framework.reverse import reverse

from backend.helper import calendar
from .base import BaseModel
from .profile import Profile, Attachment


class Agenda(BaseModel):
    name = models.CharField("event name", max_length=255)
    slug = autoslug.fields.AutoSlugField(populate_from='name', unique=True)
    location = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    start_at = models.DateField(blank=True, null=True)
    duration = models.IntegerField()
    website = models.URLField(blank=True)

    profile = models.ForeignKey(Profile, models.CASCADE)
    icon = models.ForeignKey(Attachment, models.SET_NULL, null=True, blank=True)

    def to_ical(self):
        cal = calendar()
        if self.start_at is None:
            return cal
        for session in self.session_set.exclude(start_at=None):
            cal.add_component(session.to_ical())
        return cal

    @property
    def owner(self):
        return self.profile.user

    @property
    def end_at(self):
        if not self.start_at:
            return None
        return self.start_at + timedelta(days=self.duration)

    def get_absolute_url(self):
        return reverse('agenda_detail', (self.pk,))

    def __str__(self):
        return self.name
