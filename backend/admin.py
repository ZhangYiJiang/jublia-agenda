from django.contrib import admin
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_filter = ('published',)


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    pass
