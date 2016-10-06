from django.db import models
from rest_framework.reverse import reverse

from .base import BaseModel
from .profile import Profile


class Agenda(BaseModel):
    name = models.CharField("event name", max_length=255)
    profile = models.ForeignKey(Profile)
    location = models.CharField(blank=True, max_length=255)
    published = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True)

    @property
    def owner(self):
        return self.profile.user

    def get_absolute_url(self):
        return reverse('agenda_detail', (self.pk,))

    def __str__(self):
        return self.name
