from django.db import models
from rest_framework.reverse import reverse

from .agenda import Agenda
from .base import BaseModel
from .profile import Attachment


class Speaker(BaseModel):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    profile = models.TextField(blank=True)
    position = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    company_description = models.TextField(blank=True)
    company_url = models.URLField(blank=True)

    agenda = models.ForeignKey(Agenda, models.CASCADE)
    image = models.ForeignKey(Attachment, models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('speaker_detail', args=[self.agenda.pk, self.pk])

    def __str__(self):
        return '{} - {}'.format(self.name, self.company)

    class Meta:
        unique_together = ('agenda', 'name',)
