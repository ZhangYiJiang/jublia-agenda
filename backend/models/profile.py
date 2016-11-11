from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework.reverse import reverse

from backend.helper import UniqueTokenGenerator
from .base import BaseModel


EXPIRY = timedelta(hours=6)


class Profile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    company = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(
        max_length=50,
        default=UniqueTokenGenerator('Profile', field='verification_token')
    )
    verification_expiry = models.DateTimeField(default=timezone.now)

    def send_verification_email(self, force=False):
        # Don't send out any verification email if one has been sent out in the last 5 min
        sent_recently = timezone.now() + EXPIRY - self.verification_expiry < timedelta(minutes=5)
        if not force and self.is_verified or (sent_recently and not settings.TESTING):
            return

        # Generate a new token
        token = self._meta.get_field('verification_token').get_default()

        # Construct email
        link = settings.BASE_URL + reverse('verify_email', args=[token])
        subject = _('Please verify your email address')
        message = _("Welcome to Jublia Agenda! Please verify your address using "
                    "this link: %s. If you did not sign up with us, please ignore "
                    "this email" % link)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, (self.user.email,))

        # Only update DB after send_mail, in case send_mail fails for whatever reason
        self.verification_token = token
        self.verification_expiry = timezone.now() + EXPIRY
        self.save()

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


class Attachment(BaseModel):
    profile = models.ForeignKey(Profile)
    file = models.ImageField()

    def __str__(self):
        return settings.BASE_URL + self.file.url
