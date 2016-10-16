from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from .base import BaseModel


def token_expiry():
    return timezone.now() + timedelta(hours=6)


class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    company = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=50, default=get_random_string)
    verification_expiry = models.DateTimeField(default=token_expiry)

    def send_verification_email(self):
        pass

    def __str__(self):
        return str(self.user)
