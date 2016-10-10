from datetime import timedelta

from django.db import models
from django.db.models import F
from rest_framework.reverse import reverse

from .base import BaseModel
from .profile import Profile


class Agenda(BaseModel):
    name = models.CharField("event name", max_length=255)
    profile = models.ForeignKey(Profile)
    location = models.CharField(blank=True, max_length=255)
    published = models.BooleanField(default=False)
    start_at = models.DateField(blank=True, null=True)

    @property
    def owner(self):
        return self.profile.user

    @property
    def end_at(self):
        if not self.date:
            return None

        end_at = F('duration') + F('start_at')
        latest = self.session_set.annotate(end_at=end_at)\
            .order_by('-end_at').first()
        return self.date + timedelta(minutes=latest.end_at)

    def get_absolute_url(self):
        return reverse('agenda_detail', (self.pk,))

    def __str__(self):
        return self.name
