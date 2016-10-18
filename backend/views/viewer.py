from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Viewer, Agenda
from backend.serializers import ViewerSerializer


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


class ViewerSessionList(RetrieveAPIView):
    serializer_class = ViewerSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_viewer(**self.kwargs)


class ViewerRegistrationView(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, agenda_id, token, session_id):
        viewer = get_viewer(agenda_id, token)

    def delete(self, request, agenda_id, token, session_id):
        viewer = get_viewer(agenda_id, token)
