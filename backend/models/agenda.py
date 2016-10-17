from datetime import timedelta

from django.db import models
from django.db.models import F
from rest_framework.reverse import reverse

from .base import BaseModel
from .profile import Profile


class Agenda(BaseModel):
    name = models.CharField("event name", max_length=255)
    profile = models.ForeignKey(Profile, models.CASCADE)
    location = models.CharField(blank=True, max_length=255)
    published = models.BooleanField(default=False)
    start_at = models.DateField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    @property
    def owner(self):
        return self.profile.user

    @property
    def end_at(self):
        if not self.start_at:
            return None

        if self.duration:
            return self.start_at + timedelta(days=self.duration)

        end_at = F('duration') + F('start_at')
        latest = self.session_set.filter(start_at__isnull=False)\
            .annotate(end_at=end_at)\
            .order_by('-end_at').first()
        return self.start_at + timedelta(minutes=latest.end_at)

    def get_absolute_url(self):
        return reverse('agenda_detail', (self.pk,))

    def __str__(self):
        return self.name
