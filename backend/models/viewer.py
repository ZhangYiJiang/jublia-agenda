from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework.reverse import reverse

from backend.helper import UniqueTokenGenerator
from .agenda import Agenda
from .base import BaseModel
from .session import Session

TIME_BETWEEN_EMAIL = timedelta(minutes=20)


class Viewer(BaseModel):
    email = models.EmailField()
    token = models.CharField(
        max_length=30,
        unique=True,
        default=UniqueTokenGenerator('Viewer'),
    )
    last_email_at = models.DateTimeField(blank=True, null=True)

    agenda = models.ForeignKey(Agenda)
    sessions = models.ManyToManyField(Session, through='Registration')

    def link(self):
        return settings.BASE_URL + '/public/agenda/{}/{}'.format(self.agenda.pk, self.token)

    def send_agenda_email(self):
        # Don't send out the mail if it has been less than the minimum time
        sent_recently = self.last_email_at is not None and timezone.now() - self.last_email_at < TIME_BETWEEN_EMAIL
        if not settings.TESTING and sent_recently:
            return
        # TODO: Get this URL from the front end
        link = self.link()
        subject = _('Your personalized agenda to %s' % self.agenda.name)
        message = _("Welcome to %(title)s! Here's a link to your personalized "
                    "event agenda: %(link)s." % {'title': self.agenda.name, 'link': link})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, (self.email,))

        # Only update DB after send_mail
        self.last_email_at = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('viewer_sessions', [self.agenda.pk, self.token])

    def __str__(self):
        return self.email

    class Meta:
        unique_together = ('email', 'agenda',)


class Registration(models.Model):
    viewer = models.ForeignKey(Viewer)
    session = models.ForeignKey(Session)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('viewer', 'session',)
