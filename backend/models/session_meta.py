from django.db import models
from django.db.transaction import atomic
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from .agenda import Agenda
from .base import BaseModel


class Track(BaseModel):
    name = models.CharField(max_length=120)
    agenda = models.ForeignKey(Agenda, models.CASCADE)

    def get_absolute_url(self):
        return reverse('track_detail', args=(self.agenda.pk, self.pk,))

    @atomic
    def delete(self, using=None, keep_parents=False):
        if self.agenda.track_set.count() == 1:
            raise ValidationError({
                "non-field-errors": [_("The event agenda must have at least one track")],
            })

        # Move all existing sessions on this track to another one to prevent the
        # delete from cascading to them
        self.session_set.update(track=self.agenda.track_set.exclude(pk=self.pk).first())

        super().delete(using, keep_parents)

    def __str__(self):
        return self.agenda.name + ' - ' + self.name

    class Meta:
        unique_together = ('agenda', 'name',)


class Venue(BaseModel):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=30, blank=True)

    agenda = models.ForeignKey(Agenda, models.CASCADE)

    def get_absolute_url(self):
        return reverse('venue_detail', args=[self.agenda.pk, self.pk])

    def __str__(self):
        if self.unit:
            return '{} - {}'.format(self.name, self.unit)
        else:
            return self.name

    class Meta:
        unique_together = ('agenda', 'name',)
