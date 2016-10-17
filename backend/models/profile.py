from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _
from rest_framework.reverse import reverse

from .base import BaseModel


EXPIRY = timedelta(hours=6)


def token_expiry():
    return timezone.now() + EXPIRY


def generate_verify_token():
    token = get_random_string(20)
    while Profile.objects.filter(verification_token=token).count() > 0:
        token = get_random_string(20)
    return token


class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    company = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=50, default=generate_verify_token)
    verification_expiry = models.DateTimeField(default=token_expiry)

    def send_verification_email(self):
        # Don't send out any verification email if one has been sent out in the last 5 min
        sent_recently = self.verification_expiry - timezone.now() < timedelta(minutes=5)
        if self.is_verified or (sent_recently and not settings.TESTING):
            return

        # Generate a new token
        self.verification_token = generate_verify_token()
        self.verification_expiry = token_expiry()
        self.save()

        link = reverse('verify_email', args=[self.verification_token])
        subject = _('Please verify your email address')
        message = _('Verify your address using this link: %s' % link)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, (self.user.email,))

    def verify_email(self):
        if self.is_verified:
            return True

        if timezone.now() < self.verification_expiry:
            self.is_verified = True
            self.verification_token = ''
            self.save()
            return True
        else:
            self.send_verification_email()
            return False

    def __str__(self):
        return str(self.user)
