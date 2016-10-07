from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from backend.models import Speaker
from backend.permissions import IsAgendaOwnerOrReadOnly
from backend.serializers import SpeakerSerializer
from .base import AgendaContextMixin


class SpeakerList(AgendaContextMixin, ListCreateAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = SpeakerSerializer

    def get_queryset(self):
        return Speaker.objects.filter(agenda=self.kwargs['agenda_id'])


class SpeakerDetail(AgendaContextMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAgendaOwnerOrReadOnly,)
    serializer_class = SpeakerSerializer

    def get_queryset(self):
        return Speaker.objects.filter(agenda=self.kwargs['agenda_id'])
