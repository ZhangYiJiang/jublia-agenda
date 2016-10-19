from django.http import Http404
from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from backend.models import Agenda


def check_agenda_permission(agenda, request):
    if agenda.published and request.method in permissions.SAFE_METHODS:
        return True

    if agenda.profile.user == request.user:
        return True

    if request.method in permissions.SAFE_METHODS:
        raise Http404

    return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Agenda):
            return check_agenda_permission(obj, request)

        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsAgendaOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        agenda = get_object_or_404(Agenda.objects, pk=view.kwargs['agenda_id'])
        return check_agenda_permission(agenda, request)
