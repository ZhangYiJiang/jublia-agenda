from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from backend.models import Session
from backend.permissions import IsOwnerOrReadOnly, IsAgendaOwnerOrReadOnly
from backend.serializers import SessionViewSerializer, SessionUpdateSerializer
from .base import AgendaContextMixin


class SessionViewMixin(AgendaContextMixin):
    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return SessionViewSerializer
        return SessionUpdateSerializer

    def get_queryset(self):
        return Session.objects.filter(agenda=self.kwargs['agenda_id'])


class SessionList(SessionViewMixin, ListCreateAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)


class SessionDetail(SessionViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)

