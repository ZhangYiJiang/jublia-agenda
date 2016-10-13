from django.db import models
from rest_framework.reverse import reverse

from .agenda import Agenda
from .base import BaseModel


class Speaker(BaseModel):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    company_description = models.TextField(blank=True)
    company_url = models.URLField(blank=True)

    agenda = models.ForeignKey(Agenda)

    def get_absolute_url(self):
        return reverse('speaker_detail', args=[self.agenda.pk, self.pk])

    def __str__(self):
        return '{} - {} at {}'.format(self.name, self.position, self.company)
