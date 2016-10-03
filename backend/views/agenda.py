from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from backend.models import Agenda
from backend.permissions import IsOwnerOrReadOnly
from backend.serializers import AgendaSerializer
from .base import UserContextMixin


class AgendaList(UserContextMixin, ListCreateAPIView):
    serializer_class = AgendaSerializer

    def get_queryset(self):
        return Agenda.objects.filter(profile__user=self.request.user)


class AgendaDetail(RetrieveUpdateAPIView):
    queryset = Agenda.objects.all()

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = AgendaSerializer
