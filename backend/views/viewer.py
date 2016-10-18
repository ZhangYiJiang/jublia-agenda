from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Viewer, Agenda
from backend.serializers import ViewerSerializer
from .base import AgendaContextMixin


@api_view(('POST',))
@permission_classes((AllowAny,))
def create_viewer(request, agenda_id):
    serializer = ViewerSerializer(data=request.data, context={
        'agenda': get_object_or_404(Agenda.objects, pk=agenda_id),
    })

    serializer.is_valid(True)
    viewer = serializer.save()
    return Response({'token': viewer.token}, status=status.HTTP_201_CREATED)


def get_viewer(agenda_id, token):
    return get_object_or_404(Viewer.objects, agenda=agenda_id, token=token)


class ViewerSessionList(AgendaContextMixin, RetrieveAPIView):
    serializer_class = ViewerSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_viewer(**self.kwargs)


class ViewerRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, agenda_id, token, session_id):
        # This is probably a little more convoluted than it should be
        # should refactor when there's time
        agenda = get_object_or_404(Agenda.objects, pk=agenda_id)
        viewer = get_viewer(agenda_id, token)
        session = get_object_or_404(agenda.session_set, pk=session_id)
        if not viewer.registration_set.filter(session=session_id).exists():
            viewer.registration_set.create(session=session)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, agenda_id, token, session_id):
        queryset = get_viewer(agenda_id, token).sessions
        get_object_or_404(queryset, pk=session_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
