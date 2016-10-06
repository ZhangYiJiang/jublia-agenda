from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from backend.models import Session
from backend.permissions import IsOwnerOrReadOnly, IsAgendaOwnerOrReadOnly
from backend.serializers import SessionSerializer
from .base import AgendaContextMixin


class SessionList(AgendaContextMixin, ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = (IsAgendaOwnerOrReadOnly,)

    def get_queryset(self):
        return Session.objects.filter(agenda=self.kwargs['agenda_id'])


class SessionDetail(AgendaContextMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = SessionSerializer

    def get_queryset(self):
        return Session.objects.filter(agenda=self.kwargs['agenda_id'])
