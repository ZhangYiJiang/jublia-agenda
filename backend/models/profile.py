from django.db import models
from .base import BaseModel
from django.conf import settings


class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    company = models.CharField(max_length=255, blank=True)
