from django.contrib import admin

from . import models


class TagInline(admin.StackedInline):
    model = models.Tag


class TrackInline(admin.StackedInline):
    model = models.Track


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_filter = ('published',)
    inlines = (TrackInline,)


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'agenda', 'venue',)
    filter_horizontal = ('speakers',)


@admin.register(models.Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'agenda', 'company',)


@admin.register(models.Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'agenda',)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'agenda',)
    inlines = (TagInline,)


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'agenda',)


@admin.register(models.Viewer)
class ViewerAdmin(admin.ModelAdmin):
    readonly_fields = ('token',)
    filter_horizontal = ('sessions',)
