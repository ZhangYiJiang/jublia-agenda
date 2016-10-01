from django.db import models
from .base import BaseModel


class Agenda(BaseModel):
    name = models.CharField("event name", max_length=255)
    location = models.CharField(blank=True, max_length=255)
    published = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
