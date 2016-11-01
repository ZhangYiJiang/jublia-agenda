from datetime import timedelta

from django.db import models
from rest_framework.reverse import reverse

from .base import BaseModel
from .profile import Profile, Attachment


class Agenda(BaseModel):
    name = models.CharField("event name", max_length=255)
    location = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    start_at = models.DateField(blank=True, null=True)
    duration = models.IntegerField()
    website = models.URLField(blank=True)

    profile = models.ForeignKey(Profile, models.CASCADE)
    icon = models.ForeignKey(Attachment, models.SET_NULL, null=True, blank=True)

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
