from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response

from backend.models import Agenda
from backend.permissions import IsOwnerOrReadOnly, IsAgendaOwner
from backend.serializers import BaseAgendaSerializer, AgendaSerializer
from .base import UserContextMixin


class AgendaList(UserContextMixin, ListCreateAPIView):
    serializer_class = BaseAgendaSerializer

    def get_serializer_context(self):
        # Add tracks to the serializer context, if it is in the request
        context = super().get_serializer_context()
        context['tracks'] = self.request.data.get('tracks', [])
        return context

    def get_queryset(self):
        return Agenda.objects.filter(profile__user=self.request.user)


class AgendaDetail(UserContextMixin, RetrieveUpdateDestroyAPIView):
    queryset = Agenda.objects.all()

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = AgendaSerializer


@api_view(('GET',))
@permission_classes((IsAgendaOwner,))
def dirty_sessions(request, agenda_id):
    agenda = get_object_or_404(Agenda.objects, pk=agenda_id)
    sessions = agenda.session_set.filter(dirty=True).values_list('pk', flat=True)
    return Response(sessions, status.HTTP_200_OK)
