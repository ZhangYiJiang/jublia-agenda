from django.db import models

from .agenda import Agenda
from .base import BaseModel
from .session import Session


class Viewer(BaseModel):
    email = models.EmailField()
    token = models.CharField(max_length=30, unique=True)

    agenda = models.ForeignKey(Agenda)
    sessions = models.ManyToManyField(Session, through='Registration')

    def __str__(self):
        return self.email


class Registration(models.Model):
    viewer = models.ForeignKey(Viewer)
    session = models.ForeignKey(Session)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('viewer', 'session',)
