from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from backend.models import Track
from backend.permissions import IsAgendaOwnerOrReadOnly
from backend.serializers import TrackSerializer
from .base import AgendaContextMixin


class TrackList(AgendaContextMixin, ListCreateAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = TrackSerializer

    def get_queryset(self):
        return Track.objects.filter(agenda=self.kwargs['agenda_id'])


class TrackDetail(AgendaContextMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = TrackSerializer

    def get_queryset(self):
        return Track.objects.filter(agenda=self.kwargs['agenda_id'])
