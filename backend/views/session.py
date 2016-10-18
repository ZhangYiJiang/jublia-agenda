from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from backend.models import Session
from backend.permissions import IsOwnerOrReadOnly, IsAgendaOwnerOrReadOnly
from backend.serializers import SessionSerializer
from .base import AgendaContextMixin


class SessionViewMixin(AgendaContextMixin):
    serializer_class = SessionSerializer

    def get_queryset(self):
        return Session.objects.filter(agenda=self.kwargs['agenda_id'])


class SessionList(SessionViewMixin, ListCreateAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)


class SessionDetail(SessionViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)

