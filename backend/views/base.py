from rest_framework.generics import get_object_or_404

from backend.models import Agenda


class UserContextMixin:
    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'user': self.request.user,
        }


class AgendaContextMixin:
    def get_serializer_context(self):
        agenda = get_object_or_404(Agenda.objects.all(), pk=self.kwargs['agenda_id'])
        return {
            **super().get_serializer_context(),
            'agenda': agenda,
        }
