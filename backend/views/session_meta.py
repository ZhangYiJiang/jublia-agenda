from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from backend.models import Track, Speaker
from backend.permissions import IsAgendaOwnerOrReadOnly
from backend.serializers import TrackSerializer, SpeakerSerializer, BaseSpeakerSerializer
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


class SpeakerList(AgendaContextMixin, ListCreateAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = BaseSpeakerSerializer

    def get_queryset(self):
        return Speaker.objects.filter(agenda=self.kwargs['agenda_id'])


class SpeakerDetail(AgendaContextMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = SpeakerSerializer

    def get_queryset(self):
        return Speaker.objects.filter(agenda=self.kwargs['agenda_id'])
