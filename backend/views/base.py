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


class SplitSerializerMixin:
    """
    ModelViewSet mixin which splits create and list requests down one serializer,
    and retrieve, update and delete requests down the other
    """
    def get_serializer_class(self):
        if self.is_list_create_request:
            return self.list_serializer_class
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        self.is_list_create_request = kwargs.get('many', False) or self.request.method == 'POST'
        super().get_serializer(*args, **kwargs)
