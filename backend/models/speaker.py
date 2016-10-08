from django.db import models

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

    def __str__(self):
        return '{} - {} at {}'.format(self.name, self.position, self.company)