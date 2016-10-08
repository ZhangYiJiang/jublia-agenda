from rest_framework import permissions

from backend.models import Agenda


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsAgendaOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow creating and editing if you are the owner of the event
        pk = view.kwargs['agenda_id']
        return request.user.is_authenticated and \
               Agenda.objects.filter(pk=pk, profile__user=request.user).exists()
