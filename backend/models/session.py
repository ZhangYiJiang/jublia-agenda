from django.db import models
from .base import BaseModel
from .agenda import Agenda


class Session(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    agenda = models.ForeignKey(Agenda)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=255)
    agenda = models.ForeignKey(Agenda)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name
