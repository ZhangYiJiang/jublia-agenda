from django.conf import settings
from django.db import models

from .base import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    company = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.user)
